from flask import Flask
import json
import requests

app = Flask(__name__)


@app.route('/ppg/<data>')
def process_ppg(data):
    # Process the PPG data here
    return json.dumps({'Processed PPG data: ': data})

@app.route('/ppg/ask_ppg')
def ask_ppg():
    print("wat")
    ask_ppg = "http://192.168.1.84/ppg"
    received_ppg = requests.get(ask_ppg)
    print("wee")
    return json.dumps({'data': received_ppg.content})

if __name__ == '__main__':
    app.run(host='192.168.1.118', port=5000)
