import urequests as requests
import json
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

connect_wifi()
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
response = response.json() #Parse JSON response into a python dictionary
access_token = response["access_token"] #Parse access token out of the response dictionary
intervals = [828, 836, 852, 760, 800, 796, 856, 824, 808, 776, 724, 816, 800, 812, 812, 812, 756, 820, 812, 800] #Interval
#data to be sent to KuniosCloud
# Form data set as instructed in
# https://analysis.kubioscloud.com/v2/portal/documentation/api_analytics.html#analyze-a-dataset-v2
data_set = {
   "type": "PPI",
   "data": intervals,
   "analysis": {
     "type": "readiness"
               }}
                
    
# The dataset that you send will be a python dictionary that is made up of two "Key": "Pairs" and one nested d ictionary
# The dataset will need a key value pair for "type" which describes the type of data that we are sending. In this case we are
#sending RR intervals so we can set type as "RRI"
# The second key pair is to send the actual "data", and there we can send out intervals array, provided above
# The final part is for the "analysis" analysis will have a nested dictionary key pair value to describe the type of analysis
#that we wish to be done
# The key here is "type" (again) and the value will be "readiness" to describe the type of analysis that we want.
# The analysis member can be quite a bit more complex, but for our needs, the readiness is more than enough
#dataset creation HERE
# Make the readiness analysis with the given data
response = requests.post(
                        url = "https://analysis.kubioscloud.com/v2/analytics/analyze",
                        headers = { "Authorization": "Bearer {}".format(access_token), #use access token to access your
#KubiosCloud analysis session
                                    "X-Api-Key": APIKEY },
                        json = data_set) #dataset will be automatically converted to JSON by the urequests library
response = response.json()
#Print out the SNS and PNS values on the OLED screen
