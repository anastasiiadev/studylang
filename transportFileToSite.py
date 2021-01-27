import requests

url = 'http://httpbin.org/post'
files = {'file': open('img/S.jpg', 'rb')}
r = requests.post(url, files=files)
r.text
if r.status_code == 200:
    print('fine')
else:
    print('error')