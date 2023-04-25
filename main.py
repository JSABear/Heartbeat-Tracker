from machine import Pin
from led import Led
import time
from display import Oled

sw_0 = Pin(9, Pin.IN, Pin.PULL_UP)
sw_1 = Pin(8, Pin.IN, Pin.PULL_UP)
sw0_status = sw_0.value()
sw1_status = sw_1.value()
sw0_past_state = -1
sw1_past_state = -1
oled = Oled(1)
enter = True
menu = 1

def main_screen():
    main_screen_design()


def collect_data():
    pass


def result_screen():
    result_screen_design()

def button_listener():
    global menu, enter, sw0_past_state, sw1_past_state
    if sw0_past_state != sw_0.value or sw1_past_state != sw_1.value:
        if menu == 1 and sw_0.value() == 0: #from main menu to collect data
            sw0_past_state = sw_0.value
            enter = True
            menu = 2
            while sw_0.value() == 0:
                pass
        if menu == 1 and sw_1.value() == 0: #from main menu to past result
            sw1_past_state = sw_1.value
            enter = True
            menu = 3
            while sw_1.value() == 0:
                pass
            
        if menu == 2 and sw_0.value() == 0: #from collect data to cancel to menu
            sw0_past_state = sw_0.value
            enter = True
            menu = 1
            while sw_0.value() == 0:
                pass
        #if menu == 2 and sw_1.value() == 0: #from collect data to results (not used in time based system)
            #sw1_past_state = sw_1.value
            #enter = True
            #menu = 3
            #while sw_1.value() == 0:
                #pass
        #if menu == 3 and sw_0.value() == 0: #from results to collect data (not used)
            #sw0_past_state = sw_0.value
            #enter = True
            #menu = 2
            #while sw_0.value() == 0:
                #pass
        if menu == 3 and sw_1.value() == 0: #from results back to menu
            sw1_past_state = sw_1.value
            enter = True
            menu = 1
            print(sw_1.value())
            while sw_1.value() == 0:
                pass

def main_screen_design():
    global enter
    if enter == True:
        oled.clear()
        oled.display_fill(1, 49, 42, 15)
        oled.display_fill(90, 49, 45, 15)
        oled.clear_control("Start", 2, 53)
        oled.clear_control("Back", 94, 53)
        enter = False
        
        
def result_screen_design():
    global enter
    if enter == True:
        oled.clear()
        oled.display_control("60   BPM", 5, 5)
        oled.display_control("010  Stress", 5, 17)
        oled.display_control("101  Recovery", 5, 30)
        oled.display_fill(90, 49, 45, 15)
        oled.clear_control("Back", 94, 53)
        enter = False    

def collect_data():
    global enter
    if enter == True:
        oled.clear()
        oled.display_control("  Collecting...", 5, 30)
        oled.display_fill(74, 49, 48, 15)
        oled.clear_control("Cancel", 75, 53)
        enter = False


while True:
    while menu == 1:
        main_screen()
        button_listener()
    while menu == 2:
        collect_data()
        button_listener()
    while menu == 3:
        result_screen()
        button_listener()
