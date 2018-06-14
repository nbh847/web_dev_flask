# coding: utf-8

import socket
import os

"""
课 2 上课用品
2017/02/16

本次上课的主要内容有
0, 请注意代码的格式和规范
1, 规范化生成响应
2, HTTP 头
3, 几个常用 HTML 标签及其用法
4, 参数传递的两种方式
"""


def log(*args, **kwargs):
    '''
    用log代替pring
    :param args:
    :param kwargs:
    :return:
    '''
    print('log', *args, **kwargs)


def route_index():
    '''
    主页的处理函数，返回主页的响应
    :return:
    '''
    header = 'HTTP/1.x 200 ok\r\nContent-Type: text/html\r\n'
    body = '<h1>Hello world</h1><img src="dog.gif"/>'
    r = header + '\r\n' + body
    return r.encode('utf-8')


def page(name):
    with open(name, encoding='utf-8') as f:
        return f.read()


def route_msg():
    '''
    msg 页面处理函数
    :return:
    '''
    header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n'
    body = page('html_basic.html')
    r = header + '\r\n' + body
    return r.encode('utf-8')


def route_image():
    '''
    图片的处理函数，读取图片并生成响应返回
    :return:
    '''
    current_path = os.getcwd()
    with open(current_path + '/doge.gif', 'rb') as f:
        header = b'HTTP/1.x 200 ok\r\nContent-Type: image/gif\r\n\r\n'
        img = header + f.read()
        return img


def error(code=404):
    '''
    根据code返回不同的错误响应
    :param code:
    :return:
    '''
    e = {
        404: b'HTTP/1.1 404 NOT FOUND\r\n\r\n<h1>NOT FOUND</h1>',
    }
    return e.get(code, b'')


def response_for_path(path):
    '''
    根据path调用响应的处理函数
    没有处理的path返回404
    :param path:
    :return:
    '''
    r = {
        '/': route_index,
        '/doge.gif': route_image,
        '/msg': route_msg,
    }
    response = r.get(path, error)
    return response()


def run(host='', port=3000):
    '''
    启动服务器
    :param host:
    :param part:
    :return:
    '''
    # 初始化socket
    # 使用with保证程序中断后正确关闭socket释放端口
    with socket.socket() as s:
        s.bind((host, port))
        while True:
            s.listen(5)
            connection, address = s.accept()
            request = connection.recv(1024)
            log('raw, ', request)
            request = request.decode('utf-8')
            log('ip and request, {}\n{}'.format(address, request))
            try:
                path = request.split()[1]
                response = response_for_path(path)
                connection.send(response)
            except Exception as e:
                log('error', e)
            connection.close()


def main():
    config = dict(
        host='',
        port=3000,
    )
    run(**config)


if __name__ == '__main__':
    main()
