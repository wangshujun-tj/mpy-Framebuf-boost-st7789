import time
from machine import Pin, SPI
spi = SPI(1, 20000000, sck=Pin(27), mosi=Pin(26), miso=Pin(34))
from st7789 import ST7789
#lcd = ST7789(135, 240, spi,dc=Pin(25),cs=Pin(32),rst=Pin(33),rot=0,bgr=0)#横屏初始化
lcd = ST7789(240, 135, spi,dc=Pin(25),cs=Pin(32),rst=Pin(33),rot=1,bgr=0)#横屏初始化
lcd.font_load("GBK-32.fon")
#加载的字库是中文，可以选12，16，24，32四种中文
for count in range(10):
    lcd.fill(0)
    lcd.show_bmp("logo-2.bmp",50*(count%8),40*(count%8))
    lcd.font_set(0x11,0,1,0)
    #字体(第一位1-4对应标准，方头，不等宽标准，不等宽方头，第二位1-4对应12，16，24，32高度)，旋转，放大倍数，反白显示
    lcd.text("Micropython中文甒甒%d"%count,0,0,0xf800)
    lcd.font_set(0x12,0,1,1)
    lcd.text("micro拷贝甓甓",0,16,0x07e0)
    lcd.font_set(0x13,0,1,0)
    lcd.text("甒字符串Mpy%3.3d"%count,0,32,lcd.rgb(0,0,255))
    #lcd.rgb()是方便设置显示颜色的小功能
    lcd.font_set(0x44,0,1,0)
    lcd.text("甓中文Mpy%3.3d"%count,0,100,0x001f)
    lcd.font_set(0x23,0,1,0)
    lcd.text("中文显示Mpy%3.3d"%count,0,175,0x07e0)
    lcd.text("Mpy%3.3d"%count,0,240,0xf800)
    lcd.show()
    #lcd.save_bmp("b-%d.bmp"%count)
lcd.font_free()
