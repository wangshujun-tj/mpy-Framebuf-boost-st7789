from time import sleep_ms
from ustruct import pack
from machine import SPI,Pin
from micropython import const
import framebuf


# commands
NOP = const(0x00)
SWRESET = const(0x01)
RDDID = const(0x04)
RDDST = const(0x09)

SLPIN = const(0x10)
SLPOUT = const(0x11)
PTLON = const(0x12)
NORON = const(0x13)

INVOFF = const(0x20)
INVON = const(0x21)
DISPOFF = const(0x28)
DISPON = const(0x29)
CASET = const(0x2A)
RASET = const(0x2B)
RAMWR = const(0x2C)
RAMRD = const(0x2E)

PTLAR = const(0x30)
COLMOD = const(0x3A)
MADCTL = const(0x36)

class ST7789(framebuf.FrameBuffer):
    def __init__(self, width, height, spi, dc, rst, cs, rot=0, bgr=0, external_vcc=False):
        if dc is None:
            raise RuntimeError('ILI9341 must be initialized with a dc pin number')
        dc.init(dc.OUT, value=0)
        if cs is None:
            raise RuntimeError('ILI9341 must be initialized with a cs pin number')
        cs.init(cs.OUT, value=1)
        if rst is not None:
            rst.init(rst.OUT, value=1)
        else:
            self.rst =None
        self.spi = spi
        self.dc = dc
        self.rst = rst
        self.cs = cs
        self.height = height
        self.width = width
        self.external_vcc = external_vcc
        self.buffer = bytearray(self.height * self.width*2)
        super().__init__(self.buffer, self.width, self.height, framebuf.RGB565SW, self.width)
        self.reset()
        if rot==0:
            madctl=0x00
            self.xstart = 52
            self.ystart = 40
        elif rot==1:
            madctl=0xA0
            self.xstart = 40
            self.ystart = 52
        elif rot==2:
            madctl=0xc0
            self.xstart = 53
            self.ystart = 40
        else:
            madctl=0x60
            self.xstart = 40
            self.ystart = 52
        if bgr==1:
            madctl|=0x08
        self._write(SLPOUT)
        for command, data in((COLMOD,b'\x05'),(MADCTL,pack('>B', madctl))):
            self._write(command, data)
        self._write(INVON)
        self._write(SLPOUT)
        sleep_ms(120)
        self._write(DISPON)
        sleep_ms(50)
    def reset(self):
        if self.rst is None:
            self._write(SWRESET)
            sleep_ms(50)
            return
        self.rst.off()
        sleep_ms(50)
        self.rst.on()
        sleep_ms(50)
    def _write(self, command, data = None):
        self.cs.off()
        self.dc.off()
        self.spi.write(bytearray([command]))
        self.cs.on()
        if data is not None:
            self.cs.off()
            self.dc.on()
            self.spi.write(data)
            self.cs.on()
    def show(self):
        self._write(CASET,pack(">HH", self.xstart, self.xstart+self.width-1))
        self._write(RASET,pack(">HH", self.ystart, self.ystart+self.height-1))
        self._write(RAMWR,self.buffer)
    def rgb(self,r,g,b):
        return ((r&0xf8)<<8)|((g&0xfc)<<3)|((b&0xf8)>>3)


        

        
