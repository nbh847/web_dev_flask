# coding: utf-8

import socket
import ssl

"""
2017/02/16
作业 1


资料:
在 Python3 中，bytes 和 str 的互相转换方式是
str.encode('utf-8')
bytes.decode('utf-8')

send 函数的参数和 recv 函数的返回值都是 bytes 类型
其他请参考上课内容, 不懂在群里发问, 不要憋着
"""


# 1
# 补全函数
def protocol_of_url(url):
    '''
    url 是字符串, 可能的值如下
    'g.cn'
    'g.cn/'
    'g.cn:3000'
    'g.cn:3000/search'
    'http://g.cn'
    'https://g.cn'
    'http://g.cn/'

    返回代表协议的字符串, 'http' 或者 'https'
    '''
    return url.split(':')[0] if 'http' in url else 'http'


# 2
# 补全函数
def host_of_url(url):
    '''
    url 是字符串, 可能的值如下
    'g.cn'
    'g.cn/'
    'g.cn:3000'
    'g.cn:3000/search'
    'http://g.cn'
    'https://g.cn'
    'http://g.cn/'

    返回代表主机的字符串, 比如 'g.cn'
    '''
    if 'http' in url:
        host = url.split('/')[2]
    else:
        host = url.split(':')[0].replace('/', '')
    return host


# 3
# 补全函数
def port_of_url(url):
    '''
    url 是字符串, 可能的值如下
    'g.cn'
    'g.cn/'
    'g.cn:3000'
    'g.cn:3000/search'
    'http://g.cn'
    'https://g.cn'
    'http://g.cn/'

    返回代表端口的字符串, 比如 '80' 或者 '3000'
    注意, 如上课资料所述, 80 是默认端口
    '''
    host = host_of_url(url)
    right_url = url.split(host)[1]
    return right_url.split(':')[1].split('/')[0] if ':' in right_url else '80'


# 4
# 补全函数
def path_of_url(url):
    '''
    url 是字符串, 可能的值如下
    'g.cn'
    'g.cn/'
    'g.cn:3000'
    'g.cn:3000/search'
    'http://g.cn'
    'https://g.cn'
    'http://g.cn/'

    返回代表路径的字符串, 比如 '/' 或者 '/search'
    注意, 如上课资料所述, 当没有给出路径的时候, 默认路径是 '/'
    '''
    port = port_of_url(url)
    host = host_of_url(url)
    if port is '80':
        path = url.split(host)[1]
        return path if path else '/'
    else:
        path = url.split(port)[1]
        return path if path else '/'


# 5
# 补全函数
def parsed_url(url):
    '''
    url 是字符串, 可能的值如下
    'g.cn'
    'g.cn/'
    'g.cn:3000'
    'g.cn:3000/search'
    'http://g.cn'
    'https://g.cn'
    'http://g.cn/'
    返回一个 tuple, 内容如下 (protocol, host, port, path)
    '''
    # 检查协议
    protocol = 'http'
    if url[:7] == 'http://':
        u = url.split('://')[1]
    elif url[:8] == 'https://':
        u = url.split('://')[1]
        protocol = 'https'
    else:
        u = url

    # path
    if '/' in u:
        path = '/' + u.split('/')[1]
        host = u.split(path)[0]
    else:
        path = '/'
        host = u

    port_dict = {
        'http': 80,
        'https': 443,
    }

    # port
    port = port_dict[protocol]
    if ':' in host:
        my_host = host.split(':')
        host = my_host[0]
        port = my_host[1]

    return protocol, host, int(port), path


def socket_by_protocol(protocol):
    if protocol == 'http':
        s = socket.socket()
    else:
        s = ssl.wrap_socket(socket.socket())
    return s


def response_by_socket(s):
    response = b''
    buffer_size = 1024
    while True:
        r = s.recv(buffer_size)
        if len(r) == 0:
            break
        response += r
    return response


def parsed_response(r):
    header, body = r.split('\r\n\r\n', 1)
    header_split = header.split('\r\n')
    status_code = int(header_split[0].split()[1])
    headers = header_split[1:]
    dict_headers = {}
    for h in headers:
        s = h.split(':', 1)
        dict_headers[s[0]] = s[1].strip()

    return status_code, dict_headers, body


# 6
# 把向服务器发送 HTTP 请求并且获得数据这个过程封装成函数
# 定义如下
def get(url):
    '''
    本函数使用上课代码 client.py 中的方式使用 socket 连接服务器
    获取服务器返回的数据并返回
    注意, 返回的数据类型为 bytes
    '''
    protocol, host, port, path = parsed_url(url)
    s = socket_by_protocol(protocol)
    s.connect((host, port))

    http_request = 'GET {} HTTP/1.1\r\nhost:{}\r\nConnection: close\r\n\r\n'.format(path, host)
    request = http_request.encode('utf-8')
    s.send(request)

    response = response_by_socket(s)
    status_code, headers, body = parsed_response(response.decode('utf-8'))
    return status_code, headers, body


# 使用
def main():
    url = 'http://movie.douban.com/top250'
    status_code, headers, body = get(url)
    if status_code == 301:
        url = headers['Location']
        status_code, headers, body = get(url)
    print(status_code, headers, body)


# 单元测试，test开头
def test_parsed_url():
    http = 'http'
    https = 'https'
    host = 'g.cn'
    path = '/'
    test_items = [
        ('http://g.cn', (http, host, 80, path)),
        ('http://g.cn/', (http, host, 80, path)),
        ('http://g.cn:90', (http, host, 90, path)),
        ('http://g.cn:90/', (http, host, 90, path)),
        ('https://g.cn', (https, host, 443, path)),
        ('https://g.cn:233/', (https, host, 233, path)),
    ]
    for t in test_items:
        url, expected = t
        # print('test url: {}'.format(url))
        u = parsed_url(url)
        e = "parsed_url Error, ({}) ({}) ({})".format(url, u, expected)
        assert u == expected, e


def test_parsed_response():
    response = 'HTTP/1.1 301 Moved Permanently\r\n' \
               'Content-Type: text/html\r\n' \
               'Location: https://movie.douban.com/top250\r\n' \
               'Content-Length: 178\r\n\r\n' \
               'test body'
    status_code, header, body = parsed_response(response)
    assert status_code == 301
    assert len(list(header.keys())) == 3
    assert body == 'test body'


def test_get():
    urls = [
        'http:movie.douban.com/top250',
        'https:movie.douban.com/top250',
    ]
    for u in urls:
        get(u)


def test():
    test_parsed_url()
    test_get()
    test_parsed_response()


if __name__ == '__main__':
    # test_parsed_url()
    main()
