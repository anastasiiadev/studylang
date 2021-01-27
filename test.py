import requests
#import flask
#from flask.Flask import flask.jsonify


url = "https://terrasoft.sibset.ru/auth/get-token"
payload = {'username':'chatbot',
    'password':'c57CgRt4KW'}
files = []
headers = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate',
    'Content-Type': 'multipart/form-data; boundary=<calculated when request is sent>',
    'Content-Length': '287',
    'Connection': 'keep-alive',
    'Content-Disposition': 'form-data; name="username"',
    'Content-Disposition': 'form-data; name="password"'
}
response = requests.request('post', url, headers=headers, data=payload, files=files)
result = response.text


if response.status_code == 200:
    print('Success!')
elif response.status_code == 404:
    print('Not Found.')

'''if response == 200:
    print('yes')
        #
        #return flask.jsonify(
            #{'result':result}
        #)
else:
    print('no')
        #return flask.jsonify(
         #   {'result':'error'}
        #)'''
