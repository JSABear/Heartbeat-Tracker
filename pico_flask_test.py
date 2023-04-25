import urequests as requests
import time
import json
from wifi_connect import connect_wifi as connect
import socket
import network

table = "10"
#data = table


url = "http://192.168.1.118:5000/ppg/10"
def open_socket(ip):
    # Open a socket
    address = (ip, 80)
    connection = socket.socket()
    connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    connection.bind(address)
    connection.listen(1)
    
    
    return connection

def serve(connection):
    #Start a web server
    state = 'OFF'
    #pico_led.off()
    #temperature = 0
    while True:
        client = connection.accept()[0]
        request = client.recv(1024)
        request = str(request)
        try:
            request = request.split()[1]
        except IndexError:
            print("ree")
            pass
        if request == '/ppg?':
            #pico_led.on()
            state = 'sending ppg...'
            print("memes")
        return json.dumps({'Processed PPG data: ': 'memes'})
        #temperature = pico_temp_sensor.temp
        html = "ass"
        client.send(html)
        client.close()



try:
    ip = connect()
    connection = open_socket(ip)
    serve(connection)
except KeyboardInterrupt:
    machine.reset()
    
