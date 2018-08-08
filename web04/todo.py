from models import Model
from utils import log


# 继承自 Model 的 Todo 类
class Todo(Model):
    def __init__(self, form):
        log('Todo model form: {}'.format(form))
        self.id = form.get('id', None)
        self.title = form.get('title', '')
        self.user_id = int(form.get('user_id', -1))
        # 还应该增加 时间 等数据
