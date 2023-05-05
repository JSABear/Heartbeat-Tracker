import network
import ujson
import time
from machine import Pin
import urequests as requests


    
def send_data(ppi,sns,pns):    
    value = {
            'ppi_list': ppi,
            'sns': sns,
            'pns': pns
            }
    data_bytes = ujson.dumps(value).encode('utf-8')
    headers = {'Content-Type': 'application/json'}
    ask_ppg = f'http://192.168.101.32:8000/ppg' 
    req = requests.post(ask_ppg, data = data_bytes, headers = headers)
    print(req.status_code)
    return 





        