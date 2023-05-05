from flask import Flask, request
import json
import requests

from dbhandle import db_handler

app = Flask(__name__)


@app.route('/ppg', methods=['POST'])
def process_ppg():
   # print(request)
    data = request.get_json()
   # print(data)
    #print(type(data))
    ppi = data.get('ppi_list')
    sns = data.get('sns')
    pns = data.get('pns')
    db_handler(ppi,sns,pns)
  #  print(ppi)
   # print(sns, pns)
    return 'done'

#@app.route('/ppg_results')
#def spice_it_up(list):
 #   avg = sum(list)/len(list)
  #  print("done")
   # return avg



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)