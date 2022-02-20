import requests
import json

r = requests.get(f'https://free.currconv.com/api/v7/convert?q=USD_EUR&compact=ultra&apiKey=35dd6c11227e9eb6094a')
text = json.loads(r.content)['USD_EUR']
print(text)
print(type(text))
x = 'Доллар'
print(x.lower())
