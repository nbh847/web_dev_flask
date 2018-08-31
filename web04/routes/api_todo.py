import json
from routes.session import session
from utils import (
    log,
    redirect,
    http_response,
    json_response,
)
from models.todo import Todo
from models.weibo import Weibo


def all_weibo(request):
    """
    返回所有 weibo
    """
    ms = Weibo.all()
    # 要转换为 dict 格式才行
    data = [m.json() for m in ms]
    return json_response(data)


def add_weibo(request):
    """
    接受浏览器发过来的添加 weibo 请求
    添加数据并返回给浏览器
    """
    # 得到浏览器发送的表单, 浏览器用 ajax 发送 json 格式的数据过来
    # 所以这里我们用新增加的 json 函数来获取格式化后的 json 数据
    form = request.json()
    print('api add form', form)
    # 创建一个 weibo
    t = Weibo.new(form)
    # 把创建好的 weibo 返回给浏览器
    return json_response(t.json())


def delete_weibo(request):
    form = request.json()
    print('delete weibo form: ', form)
    weibo_id = form['weibo_id']
    Weibo.delete(weibo_id)
    print('已删除微博: ', weibo_id)
    return


def update_weibo(request):
    """
    接受浏览器发过来的更新 weibo 请求
    添加数据并返回给浏览器
    """
    # 得到浏览器发送的表单, 浏览器用 ajax 发送 json 格式的数据过来
    # 所以这里我们用新增加的 json 函数来获取格式化后的 json 数据
    form = request.json()
    print('api update form', form)
    weibo_id = form['id']
    weibo_content = form['content']
    # 创建一个 weibo
    w = Weibo.find_by(id=weibo_id)
    w.content = weibo_content
    w.save()
    # 把创建好的 weibo 返回给浏览器
    return ''


# 本文件只返回 json 格式的数据
# 而不是 html 格式的数据
def all(request):
    """
    返回所有 todo
    """
    todo_list = Todo.all()
    # 要转换为 dict 格式才行
    todos = [t.json() for t in todo_list]
    return json_response(todos)


def add(request):
    """
    接受浏览器发过来的添加 todo 请求
    添加数据并返回给浏览器
    """
    # 得到浏览器发送的表单, 浏览器用 ajax 发送 json 格式的数据过来
    # 所以这里我们用新增加的 json 函数来获取格式化后的 json 数据
    form = request.json()
    print('api add form', form)
    # 创建一个 todo
    t = Todo.new(form)
    # 把创建好的 todo 返回给浏览器
    return json_response(t.json())


def delete(request):
    """
    通过下面这样的链接来删除一个 todo
    /delete?id=1
    """
    todo_id = int(request.query.get('id'))
    t = Todo.delete(todo_id)
    return json_response(t.json())


def update(request):
    # header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n'
    form = request.json()
    todo_id = int(form.get('id'))
    t = Todo.update(todo_id, form)
    return json_response(t.json())


route_dict = {
    '/api/todo/all': all,
    '/api/todo/add': add,
    '/api/todo/delete': delete,
    '/api/todo/update': update,
    # weibo
    '/api/weibo/all': all_weibo,
    '/api/weibo/add': add_weibo,
    '/api/weibo/delete': delete_weibo,
    '/api/weibo/update': update_weibo,
}
