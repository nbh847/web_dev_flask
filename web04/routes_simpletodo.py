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


def index(request):
    """
    todo 首页的路由函数
    """
    todo_list = Todo.all()
    body = template('simple_todo_index.html', todos=todo_list)
    return http_response(body)


def edit(request):
    """
    edit 首页的路由函数, 返回edit响应
    """
    todo_id = int(request.query.get('id', -1))
    t = Todo.find_by(id=todo_id)
    body = template('simple_todo_edit.html', todo=t)
    return http_response(body)


def add(request):
    """
    用于增加新 todo 的路由函数
    """
    form = request.form()
    t = Todo.new(form)
    t.save()
    # 浏览器发送数据过来被处理后, 重定向到首页
    # 浏览器在请求新首页的时候, 就能看到新增的数据了
    return redirect('/')


def update(request):
    # 更新一个 TODO
    todo_id = int(request.query.get('id', -1))
    t = Todo.find_by(id=todo_id)
    form = request.form()
    t.task = form.get('task', '')
    t.save()
    return redirect('/')


def delete(request):
    # 得到当前编辑的 todo 的 id
    todo_id = int(request.query.get('id', -1))
    Todo.delete(todo_id)
    return redirect('/')


# 路由字典
# key 是路由(路由就是 path)
# value 是路由处理函数(就是响应)
route_dict = {
    # GET 请求, 显示页面
    '/': index,
    '/add': add,
    # POST 请求, 处理数据
    '/edit': edit,
    '/update': update,
    '/delete': delete,
}
