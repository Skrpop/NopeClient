import requests
import socketio

data = {"username": "Kerim", "password": "123456"}

url = 'https://nope-server.azurewebsites.net/api/auth/login'

response = requests.post(url, json=data)

print(response.json()['accessToken'])

accessToken = response.json()['accessToken']

sio = socketio.Client()

@sio.event
def connect():
    print('connection established')

@sio.event
def my_message(data):
    print('message received with ', data)
    sio.emit('my response', {'response': 'my response'})

@sio.event
def disconnect():
    print('disconnected from server')

sio.connect('https://nope-server.azurewebsites.net', namespaces='/', auth={'token' : accessToken})
sio.wait()