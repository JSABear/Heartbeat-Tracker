from machine import Pin
from led import Led
import time
from display import Oled
from collector import collect_data, bpm_calc, make_ppi
from wifi_connect import connect_wifi, ask_wifi
import network
from analysis import kubios_call, kubios_backup

main_3_3v = Pin(1, Pin.IN)
alt_3_3v = Pin(0, Pin.IN)

main_past_state = 0
alt_past_state = 0

sw_0 = Pin(9, Pin.IN, Pin.PULL_UP)
sw_1 = Pin(8, Pin.IN, Pin.PULL_UP)
sw0_status = main_3_3v.value()
sw1_status = alt_3_3v.value()
sw0_past_state = -1
sw1_past_state = -1
oled = Oled(1)
enter = True
menu = 0
results = None
analyzed_kubios = None

#Menu function assignment-------------------------------------------------------------------------------------------------------------#

def boot_screen():
    global menu, enter
    
    boot_screen_design()
    enter = True
    menu = 1


def main_screen():
    main_screen_design()
    

def collecting_screen():
    global menu, enter, results, oled, ppi_list
    countdown(5)
    collecting_data_design()
    received_data = collect_data(30)
    results = received_data[0]
    ppi_list = received_data[1]
    print(ppi_list)
    enter = True
    menu = 3

def analyzing_screen():
    global menu, enter, results, ppi_list, analyzed_local, analyzed_kubios
    
    if enter == True:
        print(results)
        
    analyzing_data_design()
    
    if len(ppi_list) > 10:
        analyzed_kubios = kubios_call(ppi_list)
    analyzed_local = kubios_backup(ppi_list)
    
    enter = True
    menu = 4

def result_screen():
    global results, analyzed_local, analyzed_kubios
    
    if results != None:
        result_screen_design(results, analyzed_local[1], analyzed_local[2])
    else: 
        result_screen_design("--", "--", "--")

def result_screen_2():
    global results, analyzed_local, analyzed_kubios
    
    if analyzed_kubios != None:
        sns = f"{(analyzed_kubios[0]):.2f}"
        pns = f"{(analyzed_kubios[1]):.2f}"
        result_screen_2_design(sns, pns)
    else: 
        result_screen_2_design("--", "--")
    
#Visual designs on Oled-----------------------------------------------------------------------------------------------------------#
    
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

def countdown(num):
    if enter == True:
        count = num
        for n in range(count):
            oled.display_control(f"{count}", 60, 20)
            time.sleep(1)
            oled.clear_control(f"{count}", 60, 20)
            count -= 1
        

def collecting_data_design():
    global enter
    
    if enter == True:
        oled.clear()
        oled.display_control("  Collecting...", 5, 30)
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

def result_screen_design(bpm, sdnn, rmssd):
    global enter
    
    if enter == True:
        oled.clear()
        oled.display_control(f"{bpm}     BPM", 5, 5)
        oled.display_control(f"{sdnn}    SDNN", 5, 17)
        oled.display_control(f"{rmssd}   RMSSD", 5, 30)
        oled.display_fill(1, 49, 42, 15)
        oled.clear_control("More", 2, 53)
        oled.display_fill(90, 49, 45, 15)
        oled.clear_control("Back", 94, 53)
        enter = False

def result_screen_2_design(sns, pns):
    global enter
    
    if enter == True:
        oled.clear()
        oled.display_control(f"{sns}   Stress", 5, 5)
        oled.display_control(f"{pns}  Recovery", 5, 17)
        oled.display_fill(1, 49, 42, 15)
        oled.clear_control("More", 2, 53)
        oled.display_fill(90, 49, 45, 15)
        oled.clear_control("Back", 94, 53)
        enter = False

#Handling button presses-----------------------------------------------------------------------------------------------------#

def button_listener():
    global menu, enter, sw0_past_state, sw1_past_state
    
    if sw0_past_state != main_3_3v.value() or sw1_past_state != alt_3_3v.value():
        if menu == 1 and main_3_3v.value() == 1: #from main menu to collect data
            sw0_past_state = main_3_3v.value()
            enter = True
            menu = 2
            while main_3_3v.value() == 1:
                pass
        if menu == 1 and alt_3_3v.value() == 1: #from main menu to past result
            sw1_past_state = alt_3_3v.value()
            enter = True
            menu = 4
            while alt_3_3v.value() == 1:
                pass
            
        if menu == 2 and main_3_3v.value() == 1: #from collect data to cancel to menu
            sw0_past_state = main_3_3v.value()
            enter = True
            menu = 1
            while main_3_3v.value() == 1:
                pass
            
        if menu == 3 and alt_3_3v.value() == 1: #from analyzing back to menu
            sw1_past_state = alt_3_3v.value()
            enter = True
            menu = 1
            while alt_3_3v.value() == 1:
                pass
            
        if menu == 4 and main_3_3v.value() == 1: #from results second page
            sw1_past_state = main_3_3v.value()
            enter = True
            menu = 5
            while main_3_3v.value() == 1:
                pass    
            
        if menu == 4 and alt_3_3v.value() == 1: #from results back to menu
            sw1_past_state = alt_3_3v.value()
            enter = True
            menu = 1
            while alt_3_3v.value() == 1:
                pass
            
        if menu == 5 and main_3_3v.value() == 1: #from results second page
            sw1_past_state = main_3_3v.value()
            enter = True
            menu = 4
            while main_3_3v.value() == 1:
                pass    
            
        if menu == 5 and alt_3_3v.value() == 1: #from results back to menu
            sw1_past_state = alt_3_3v.value()
            enter = True
            menu = 1
            while alt_3_3v.value() == 1:
                pass   

#Main loop-----------------------------------------------------------------------------------------------------#

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
        
    while menu == 5:
        result_screen_2()
        button_listener()