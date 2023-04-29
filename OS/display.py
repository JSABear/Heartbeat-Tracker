from machine import Pin, I2C
import ssd1306
import framebuf

i2c = I2C(1, sda=Pin(14), scl=Pin(15),freq=400000)
display = ssd1306.SSD1306_I2C(128, 64, i2c)

class Oled:
    def __init__(self, id):
        self.name = id
    
    def display_control(self, text, x, y):
        display.text(text, x, y)
        display.show()

    def display_fill(self, start_x, start_y, end_x, end_y):
        display.fill_rect(start_x, start_y, end_x, end_y, 1)
        display.show()

    def clear_control(self, text, x, y):
        display.text(text, x, y, 0)
        display.show()

    def clear(self):
        display.fill(0)
        display.show()
        
    def pixel(self, x, y, c):
        display.pixel(x, y, c)
        display.show()
    
    def display_rect(self, start_x, start_y, end_x, end_y):
        display.rect(start_x, start_y, end_x, end_y, 1)
    
    def show_screen(self):
        display.show()