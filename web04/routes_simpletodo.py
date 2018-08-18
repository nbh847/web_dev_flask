from utils import log
from models import Todo
from models import User
from routes_user import current_user
from utils import template
from utils import redirect
from utils import http_response


def login_required(route_function):
    def f(request):
        uname = current_user(request)
        u = User.find_by(username=uname)
        if u is None:
            return redirect('/login')
        return route_function(request)

    return f


from models import Todo


# 直接写函数名字不写 route 了
def index(request):
    """
    主页的处理函数, 返回主页的响应
    """
    todo_list = Todo.all()
    body = template('simple_todo_index.html', todos=todo_list)
    return http_response(body)


def add(request):
    """
    接受浏览器发过来的添加 todo 请求
    添加数据并发一个 302 定向给浏览器
    浏览器就会去请求 / 从而回到主页
    """
    todo_list = Todo.all()
    body = template('simple_todo_index.html', todos=todo_list)
    return http_response(body)


def edit(request):
    '''
    edit 页的处理函数，返回 edit 页的响应
    /edit?id=1
    '''
    todo_id = int(request.query.get('id', -1))
    t = Todo.find_by(id=todo_id)
    body = template('simple_todo_edit.html', todo=t)
    return http_response(body)


def update(request):
    # 更新一个 TODO
    todo_id = int(request.query.get('id', -1))
    t = Todo.find_by(id=todo_id)
    form = request.form()
    t.task = form.get('task', '')
    t.save()
    return redirect('/')


def delete(request):
    """
    通过下面这样的链接来删除一个 todo
    /delete?id=1
    """
    todo_id = int(request.query.get('id'))
    Todo.delete(todo_id)
    return redirect('/')


route_dict = {
    # POST 请求, 处理数据
    '/': index,
    '/add': add,
    '/edit': edit,
    '/update': update,
    '/delete': delete,
}
