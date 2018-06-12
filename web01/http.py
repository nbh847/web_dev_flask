import socket

host = ''
port = 2000
s = socket.socket()
s.bind((host, port))

while True:
    s.listen(5)
    connection, address = s.accept()
    request = connection.recv(1023)

    print('ip and request, {}\n{}'.format(address, request.decode('utf-8')))
    response = b'<html lang="en"><body class="hold"><h1>hello world</h1></body></html>'
    connection.sendall(response)
    connection.close()
