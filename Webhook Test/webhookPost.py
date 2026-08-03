import requests
import json

webhook_url = 'https://wai-dicotyledonous-pauselessly.ngrok-free.dev/discCompress/webhook'

data = { 'user' :'Bread1__1',
        'message' : 'Hello!'}

r = requests.post(webhook_url, data= json.dumps(data),headers={'Content-Type':'application/json'})