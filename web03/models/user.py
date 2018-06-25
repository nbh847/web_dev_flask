from models import Model
import os
import json
from utils import log


class User(Model):
    def __init__(self, form):
        self.username = form.get('username', '')
        self.password = form.get('password', '')

    def validate_login(self):
        log('login', self.username, self.password)
        path = os.getcwd() + '/db/User.txt'
        with open(path, 'r', encoding='utf-8') as f:
            data = f.read()
            if data:
                dic = json.loads(data)
                log('dic', dic)
                for item in dic:
                    log('each username', item)
                    if self.username == item['username'] and self.password == item['password']:
                        log('login success')
                        return True
        log('login failed')
        return False

    def validate_register(self):
        log('register', self.username, self.password)
        path = os.getcwd() + '/db/User.txt'
        pwd_form = {
            'username': self.username,
            'password': self.password,
        }
        data = self.load(path)
        if data:
            data = json.loads(data)
            for m in data:
                if self.username == m['username']:
                    return False
        else:
            data = []
        data.append(pwd_form)
        log('read file closed', data)
        log('write file started')
        log('log data', data)
        log('log type of data', type(data))
        with open(path, 'w+', encoding='utf-8') as w:
            w.write(json.dumps(data))
        log('the user is valid', self.load(path))
        return True

    def get_id(self):
        path = os.getcwd() + '/db/User.txt'
        data = self.load(path)
        if data:
            flag = json.loads(data)[0]
            return flag['id'] if 'id' in flag else None
        else:
            return None

    def load(self, path):
        with open(path, 'r', encoding='utf-8') as f:
            data = f.read()
            return data
