from machine import Pin, ADC, I2C
from piotimer import Piotimer
from fifo import Fifo
import time
import utime
from display import Oled

adc = ADC(26)
samples = Fifo(750)
avg_w = 25
avg_samples = Fifo(avg_w)
beats = False
oled = Oled(1)

def read(tid):
     samples.put(adc.read_u16())
     
tmr = Piotimer(freq=250, mode=Piotimer.PERIODIC, callback=read)

bpm_list = []
l = []
utime.sleep(0.25)
ppi = 0
bpm_int = 0
bpm = 0
prev_bpm = 0
enter = True
ppi_list = [1000]
bpm_avg = 0

def make_ppi():
    global ppi, ppi_list
    bpm = 0
    if len(l) > 2:
        ppi = l[-1] - l[-2]
        if ppi != ppi_list[-1]:
            ppi_list.append(ppi)  
    return ppi_list

def bpm_calc():
    global bpm, bpm_int, ppi_list, bpm_list, bpm_avg
    
    if len(l) > 2:
        ppi = l[-1] - l[-2]
        if ppi > 500 and ppi < 1500:
            if ppi != ppi_list[-1]:
                ppi_list.append(ppi)
                bpm = 60/(ppi/1000) # equation to determine bpm 
            bpm_int = int(bpm)
            bpm_list.append(bpm_int)
            bpm_avg = round(sum(bpm_list)/len(bpm_list))
            bpm_calc_screen(bpm_int)
    #print(l)
    return bpm_avg, ppi_list

def bpm_calc_screen(value):
    global prev_bpm, enter
    if prev_bpm != value:
        oled.clear_control(f"{prev_bpm}", 45, 15)
        oled.display_control(f"{value}  BPM", 45, 15)
    if enter == True:
        oled.display_control("  Collecting...", 5, 30)
        oled.display_fill(74, 49, 48, 15)
        oled.clear_control("Cancel", 75, 53)
        enter = False
    prev_bpm = value
    return

def collect_data(run_time):
    global samples, avg, avg_samples, l, beats, bpm_list
    l = []
    bpm_list = []
    start_time = time.time()
    while True:
        current_time = time.time()
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
            
        if avg < threshold and beats == True:
            beats = False
        
        result = bpm_calc()
        
        if current_time - start_time >= run_time:
            l = []
            return result
      

    

    