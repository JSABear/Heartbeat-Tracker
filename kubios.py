import requests
import base64
import json

CLIENT_ID = 'mixu03@gmail.com'
CLIENT_SECRET = 'Viutilo1'
SCOPE = ''
basic_auth_string = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode('utf-8')).decode('utf-8')
response = requests.post(
    f'https://AUTH_DOMAIN/oauth2/token',
    headers={'Authorization': f'Basic {basic_auth_string}'},
    data={
        'client_id' : CLIENT_ID,
        'grant_type': 'client_credentials',
        'scope': SCOPE,
    },
)

token = response.json()['access_token']

API_KEY = 'key'
headers = {
    'X-Api-Key': API_KEY,
    'Authorization': f'Bearer {token}',
}
response = requests.post(
    '/v2/analytics/analyze',
    headers=headers,
    json={
        'type': 'RRI',
        'data': [1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1001],
        'analysis': {
            'type': 'readiness',
            'history': [],
        },
    },
)

result = response.json()

print(result)


