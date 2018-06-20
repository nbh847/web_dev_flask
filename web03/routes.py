from utils import log
from models import Message
from models import User


message_list = []


def template(name):
    '''
    返回模版下对应的html文件
    :param name:
    :return:
    '''
    path = 'templates/' + name
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def route_index(request):
    '''
    主页的处理函数, 返回主页的响应
    '''
    header = 'HTTP/1.1 210 VERY OK\r\nContent-Type: text/html\r\n'
    body = template('index.html')
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def route_login(request):
    header = 'HTTP/1.1 210 VERY OK\r\nContent-Type: text/html\r\n'
    if request.method == 'POST':
        form = request.form()
        u = User.new(form)
        if u.validate_login():
            result = '登录成功'
        else:
            result = '用户名或者密码错误'
    else:
        result = ''
    body = template('login.html')
    body = body.replace('{{result}}', result)