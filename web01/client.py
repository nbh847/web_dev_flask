import socket
import ssl

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s = ssl.wrap_socket(s)

host = 'g.cn'
port = 80
s.connect((host, port))

ip, port = s.getsockname()
print('本机IP 和 port : {}, {}'.format(ip, port))

http_request = 'GET / HTTP/1.1\r\nhost:{}\r\n\r\n'.format(host)
req = http_request.encode('utf-8')
print('请求', req)
s.send(req)

# receive data
response = s.recv(1024)
print('响应', response)
print('str 响应', response.decode('utf-8'))
