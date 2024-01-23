import requests

response = requests.get('http://127.0.0.1:5000/sendJson')
print(response.text)


url = 'http://127.0.0.1:5000/data'
data = {'key1': 'value1', 'key2': 'value2'}

response = requests.post(url, json=data)
print(response.text)