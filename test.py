import requests
url = 'http://localhost:3000/'
with open("test_request.json", "r") as f:
    payload = f.read()
headers = {'content-type': 'application/json'}
r = requests.post(url, data=payload, headers=headers)

print(r.json())