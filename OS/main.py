from machine import Pin
from led import Led
import time
from display import Oled
from collector import collect_data, bpm_calc, make_ppi
from wifi_connect import connect_wifi, ask_wifi
import network

sw_0 = Pin(9, Pin.IN, Pin.PULL_UP)
sw_1 = Pin(8, Pin.IN, Pin.PULL_UP)
sw0_status = sw_0.value()
sw1_status = sw_1.value()
sw0_past_state = -1
sw1_past_state = -1
oled = Oled(1)
enter = True
menu = 0

#-------------------------------------------------------------------------------------------------------------#

def boot_screen():
    global menu, enter
    boot_screen_design()
    enter = True
    menu = 1


def main_screen():
    main_screen_design()
    

def collecting_screen():
    global menu, enter, results, oled
    collecting_data_design()
    results = collect_data(15)
    enter = True
    menu = 3

def analyzing_screen():
    global menu, enter, results
    if enter == True:
        print(results)
    analyzing_data_design()
    time.sleep(2)
    enter = True
    menu = 4

def result_screen():
    global results
    result_screen_design(results)
    
#-----------------------------------------------------------------------------------------------------------#
    
def boot_screen_design():
    global enter
    while enter == True:
        oled.display_rect(41,4,44,46)
        oled.display_rect(43,6,19,20)
        oled.display_rect(43,28,19,20)
        oled.display_rect(64,6,19,20)
        oled.display_rect(64,28,19,20)
        oled.show_screen()
        enter = False
    wlan = connect_wifi()
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        oled.display_control(" Connecting.", 5, 55)
        time.sleep(1)
        oled.display_control(" Connecting..", 5, 55)
        time.sleep(1)
        oled.display_control(" Connecting...", 5, 55)
        time.sleep(1)
        oled.clear_control("            ..", 5, 55)
    ip = ask_wifi()
    enter = False
    

def main_screen_design():
    global enter
    if enter == True:
        oled.clear()
        oled.display_fill(1, 49, 42, 15)
        oled.display_fill(90, 49, 45, 15)
        oled.clear_control("Start", 2, 53)
        oled.clear_control("Back", 94, 53)
        enter = False

def collecting_data_design():
    global enter
    if enter == True:
        oled.clear()
        oled.display_control("  Collecting...", 5, 35)
        oled.display_fill(74, 49, 48, 15)
        oled.clear_control("Cancel", 75, 53)
        enter = False

def analyzing_data_design():
    global enter
    if enter == True:
        oled.clear()
        oled.display_control("  Analyzing...", 5, 30)
        oled.display_fill(74, 49, 48, 15)
        oled.clear_control("Cancel", 75, 53)
        enter = False

def result_screen_design(result):
    global enter
    if enter == True:
        oled.clear()
        oled.display_control(f"{result}   BPM", 5, 5)
        oled.display_control("010  Stress", 5, 17)
        oled.display_control("101  Recovery", 5, 30)
        oled.display_fill(90, 49, 45, 15)
        oled.clear_control("Back", 94, 53)
        enter = False

#-----------------------------------------------------------------------------------------------------#

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
            menu = 4
            while sw_1.value() == 0:
                pass
            
        if menu == 2 and sw_0.value() == 0: #from collect data to cancel to menu
            sw0_past_state = sw_0.value
            enter = True
            menu = 1
            while sw_0.value() == 0:
                pass
            
        if menu == 3 and sw_1.value() == 0: #from analyzing back to menu
            sw1_past_state = sw_1.value
            enter = True
            menu = 1
            print(sw_1.value())
            while sw_1.value() == 0:
                pass
            
        if menu == 4 and sw_1.value() == 0: #from results back to menu
            sw1_past_state = sw_1.value
            enter = True
            menu = 1
            print(sw_1.value())
            while sw_1.value() == 0:
                pass

#-----------------------------------------------------------------------------------------------------#

while True:
    while menu == 0:
        boot_screen()
        
    while menu == 1:
        main_screen()
        button_listener()
        
    while menu == 2:
        collecting_screen()
        button_listener()
        
    while menu == 3:
        analyzing_screen()
        button_listener()
        
    while menu == 4:
        result_screen()
        button_listener()
