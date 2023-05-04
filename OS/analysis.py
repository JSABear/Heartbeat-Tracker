import urequests as requests
import json


def kubios_call(intervals):
    APIKEY = "pbZRUi49X48I56oL1Lq8y8NDjq6rPfzX3AQeNo3a"
    CLIENT_ID = "3pjgjdmamlj759te85icf0lucv"
    CLIENT_SECRET = "111fqsli1eo7mejcrlffbklvftcnfl4keoadrdv1o45vt9pndlef"
    LOGIN_URL = "https://kubioscloud.auth.eu-west-1.amazoncognito.com/login"
    TOKEN_URL = "https://kubioscloud.auth.eu-west-1.amazoncognito.com/oauth2/token"
    REDIRECT_URI = "https://analysis.kubioscloud.com/v1/portal/login"
    response = requests.post(
        url = TOKEN_URL,
        data = 'grant_type=client_credentials&client_id={}'.format(CLIENT_ID),
        headers = {'Content-Type':'application/x-www-form-urlencoded'},
        auth = (CLIENT_ID, CLIENT_SECRET))
    response = response.json() 
    access_token = response["access_token"] 
    #intervals = [828, 836, 852, 760, 800, 796, 856, 824, 808, 776, 724] 


    data_set = {
       "type": "PPI",
       "data": intervals,
       "analysis": {
         "type": "readiness"
                   }}
                    
    response = requests.post(
                            url = "https://analysis.kubioscloud.com/v2/analytics/analyze",
                            headers = { "Authorization": "Bearer {}".format(access_token), 

                                        "X-Api-Key": APIKEY },
                            json = data_set)
    json_list = response.json()
    parsed_values = [json_list["analysis"]["sns_index"], json_list["analysis"]["pns_index"]]
    return parsed_values


def kubios_backup(data):
    #bpm
    hr_ppi = sum(data)/len(data)
    hr_bpm = round(60 / hr_ppi * 1000)
    #sdnn
    squared_diffs = [(x - hr_ppi)**2 for x in data]
    sum_squared_diffs = sum(squared_diffs)
    variance = sum_squared_diffs / (len(data) - 1)
    sdnn = round(variance**0.5)
    #rmssd
    squared_diffs = [(data[i] - data[i-1])**2 for i in range(1, len(data))]
    mean_squared_diffs = sum(squared_diffs) / len(squared_diffs)
    rmssd = round(mean_squared_diffs ** 0.5)
    
    return hr_bpm, sdnn, rmssd
