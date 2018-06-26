import json

from utils import log
import os


def save(data, path):
    '''
    本函数把一个 dict 或者 list 写入文件
    data 是 dict 或者 list
    path 是保存文件的路径
    '''
    # json 是一个序列化/反序列化(上课会讲这两个名词) list/dict 的库
    # indent 是缩进
    # ensure_ascii=False 用于保存中文
    log('save data', data)
    for d in data:
        if 'id' in d:
            d['id'] += 1
        else:
            d['id'] = 0
    s = json.dumps(data, indent=2, ensure_ascii=False)
    with open(path, 'w+', encoding='utf-8') as f:
        log('save', path, s, data)
        f.write(s)


def load(path):
    '''
    本函数从一个文件中载入数据并转化为 dict 或者 list
    path 是保存文件的路径
    '''
    with open(path, 'r', encoding='utf-8') as f:
        s = f.read().strip()
        log('path type', type(s))
        log('load', s)
        return json.loads(s) if s else ''


# Model 是用于储存数据的基类
class Model(object):
    # @classmethod 说明这是一个 类方法
    # 类方法的调用方式是  类名.类方法()
    @classmethod
    def db_path(cls):
        # classmethod 有一个参数是 class
        # 所以我们可以得到 class 的名字
        classname = cls.__name__
        path = '{}{}.txt'.format(os.getcwd() + '/db/', classname)
        return path

    @classmethod
    def new(cls, form):
        # 下面一句相当于 User(form) 或者 Msg(form)
        # 会初始化这个函数，调用self.__init__函数
        m = cls(form)
        return m

    @classmethod
    def all(cls):
        '''
        得到一个类的所有储存的实例
        :return:
        '''
        path = cls.db_path()
        models = load(path)
        ms = [cls.new(m) for m in models]
        return ms

    @classmethod
    def find_by(cls, **kwargs):
        """
        u = User.find_by(username='gua')

        上面这句可以返回一个 username 属性为 'gua' 的 User 实例
        如果有多条这样的数据, 返回第一个
        如果没这样的数据, 返回 None

        注意, 这里参数的名字是可以变化的, 所以应该使用 **kwargs 功能
        """
        path = cls.db_path()
        data = load(path)
        items = json.load(data) if data else ''
        for key, value in kwargs.items():
            for item in items:
                if key == item['username']:
                    my_form = {
                        'username': key,
                        'password': value,
                    }
                    return cls.new(my_form)
        return None

    @classmethod
    def find_all(cls, **kwargs):
        """
        us = User.find_all(password='123')
        上面这句可以以 list 的形式返回所有 password 属性为 '123' 的 User 实例
        如果没这样的数据, 返回 []

        注意, 这里参数的名字是可以变化的, 所以应该使用 **kwargs 功能
        """
        path = cls.db_path()
        data = load(path)
        aim_dict = []
        items = json.load(data) if data else ''
        for key, value in kwargs.items():
            for item in items:
                if value == item['password']:
                    my_form = {
                        'username': key,
                        'password': value,
                    }
                    aim_dict.append(cls.new(my_form))
        return aim_dict

    def save(self):
        '''
        save 函数用于把一个 Model 的实例保存到文件中
        '''
        models = self.all()
        log('models', models)
        models.append(self)
        # __dict__ 是包含了对象所有属性和值的字典
        l = [m.__dict__ for m in models]
        path = self.db_path()
        save(l, path)

    def __repr__(self):
        classname = self.__class__.__name__
        properties = ['{}: ({})'.format(k, v) for k, v in self.__dict__.items()]
        s = '\n'.join(properties)
        return '< {}\n{} >\n'.format(classname, s)
