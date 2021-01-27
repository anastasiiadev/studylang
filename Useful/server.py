import socket


HOST = '1-ПК'
#HOST = '0.0.0.0'
PORT = 8080
ADDR = (HOST,PORT)
#BUFSIZE = 4096

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.bind(ADDR)
sock.listen(5)

print('listening ...')

while True:
    try:
        client, addr = sock.accept()
    except KeyboardInterrupt:
        sock.close()
        break
    else:
        with open('receives_file.jpg','wb') as f:
            print('file opened')

            while True:
                data = client.recv(1024)
                print('data=%s',(data))
                if not data:
                    break
                else:
                    f.write(data)
        f.close()
        #result = client.recv(BUFSIZE)
        client.close()
        #print('Message', result.decode('utf-8'))


