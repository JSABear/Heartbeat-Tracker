from machine import Pin, ADC, I2C
from piotimer import Piotimer
from fifo import Fifo
import ssd1306
global i2c
global display
import time
import utime
from led import Led
btn0 = Pin(9, mode = Pin.IN, pull = Pin.PULL_UP)
i2c = I2C(1, sda=Pin(14), scl=Pin(15))
display = ssd1306.SSD1306_I2C(128, 64, i2c)
led1 = Led(20, Pin.OUT)
adc = ADC(26)
samples = Fifo(750)
avg_w = 25
avg_samples = Fifo(avg_w)
fifo_oled = Fifo(10)
beats = False





def read(tid):
     
     samples.put(adc.read_u16())
     
tmr = Piotimer(freq=250, mode=Piotimer.PERIODIC, callback=read)
l = []

utime.sleep(0.25)
bpm_int = 0
bpm = 0
def bpm_calc():
    global bpm, bpm_int
    bpm = 0
    
    if len(l) > 2:
        
        ppi = l[-1] - l[-2]
        bpm = 60/(ppi/1000) # equation to determine bpm 
        bpm_int = int(bpm)  
    return bpm_int
    

HEART = [
[ 0, 0, 0, 0, 0, 0, 0, 0, 0],
[ 0, 1, 1, 0, 0, 0, 1, 1, 0],
[ 1, 1, 1, 1, 0, 1, 1, 1, 1],
[ 1, 1, 1, 1, 1, 1, 1, 1, 1],
[ 1, 1, 1, 1, 1, 1, 1, 1, 1],
[ 0, 1, 1, 1, 1, 1, 1, 1, 0],
[ 0, 0, 1, 1, 1, 1, 1, 0, 0],
[ 0, 0, 0, 1, 1, 1, 0, 0, 0],
[ 0, 0, 0, 0, 1, 0, 0, 0, 0],
]
pic = [
[ 0, 0, 0, 0, 0, 0, 0, 0, 0],
[ 0, 1, 1, 0, 0, 0, 1, 1, 0],
[ 0, 1, 1, 0, 0, 0, 1, 1, 0],
[ 0, 0, 0, 0, 0, 0, 0, 0, 0],
[ 0, 0, 0, 0, 0, 0, 0, 0, 0],
[ 0, 1, 1, 0, 0, 0, 1, 1, 0],
[ 0, 0, 1, 1, 0, 1, 1, 0, 0],
[ 0, 0, 0, 1, 1, 1, 0, 0, 0],
[ 0, 0, 0, 0, 1, 0, 0, 0, 0],
]

def oled():
    display.fill(0)
    display.text("%d bpm" % bpm, 1, 30)
    for y, row in enumerate(HEART):
            for x, c in enumerate(row):
                display.pixel(x, y, c)
    display.show()

prev_bpm = 0
while True:
    if not samples.empty():
        value = samples.get()
        avg_samples.put(value)
        avg = sum(avg_samples.data)/ avg_w
        avg_samples.get()
        thres_min = min(samples.data)

        thres_max = max(samples.data)
        threshold = thres_max -(thres_max - thres_min ) * 0.25
        
        
    if avg > threshold and beats == False:
        
        beats = True
        l.append(time.ticks_ms())
        
        led1.value(1)
        
        
    if avg < threshold and beats == True:
        beats = False
        led1.value(0)
        
    if len(l) >= 2:
        bpm_calc()
        #print(round(bpm))
        if bpm_int != prev_bpm and bpm_int < 200 and bpm_int > 30:
            
            print(round(bpm_int))
            fifo_oled.put(bpm_int)
        
            oled()
            prev_bpm = bpm_int
            
    if btn0.value() == 0:
        while True:
            oled_fifo_sum = sum(fifo_oled.data) / 10
            oled_string = oled_fifo_sum
            display.fill(0)
            display.text("%d average" % oled_string, 1, 30)
            for y, row in enumerate(pic):
                    for x, c in enumerate(row):
                        display.pixel(x, y, c)
            display.show()
        

        
     
        
        
        
        
        