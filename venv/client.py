import socket


HOST = '1-ПК'
#HOST = 'localhost'
PORT = 8080
ADDR = (HOST,PORT)
BUFSIZE = 4096

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

"""
if client.send(b'Text message'):
    print("The message is sent")
else:
    print("The message is NOT sent")
"""

#filename = 'img/S.jpg'
filename = '//1-ПК/Users/1/PycharmProjects/StydyLangTest/img/S.jpg'
f = open(filename,'rb')
l = f.read(1024)

while(l):
    client.send(l)
    print('Sent ', repr(l))
    l = f.read(1024)
f.close()


client.close()