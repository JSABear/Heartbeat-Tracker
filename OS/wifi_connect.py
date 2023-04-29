import network
import secrets
import time

def connect_wifi():
    global wlan
    #Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.disconnect()
    wlan.connect(secrets.SSID, secrets.PASSWORD)
    ip = wlan.ifconfig()[0]
    
    return wlan

def ask_wifi():
    global wlan
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    return ip

