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
        path = os.getcwd() + '/web03/db/User.txt'
        with open(path, 'r') as f:
            data = f.read()
            if data:
                dic = json.loads(data)
                log('dic', dic)
                for item in data:
                    if self.username == item['username'] and self.password == item['password']:
                        log('login success')
                        return True
        log('login failed')
        return False

    def validate_register(self):
        log('register', self.username, self.password)
        path = os.getcwd() + '/web03/db/User.txt'
        pwd_form = {
            'username': self.username,
            'password': self.password,
        }
        data = self.load(path)
        if data:
            my_data = json.loads(data)
            for m in my_data:
                if self.username == m['username']:
                    return False
        else:
            data = []
        log('read file closed', data)
        log('write file started')
        log('write file started')
        log('log data', data.append(pwd_form))
        log('log type of data', type(data))
        with open(path, 'w+') as w:
            w.write(json.dumps(data.append(pwd_form)))
        log('the user is valid', self.load(path))
        return True

    def load(self, path):
        with open(path, 'r') as f:
            data = f.read()
            return data
