from models import Model
import os


class User(Model):
    def __init__(self, form):
        self.username = form.get('username', '')
        self.password = form.get('password', '')

    def validate_login(self):
        path = os.getcwd() + '/web03/db/User.txt'
        with open(path, 'r') as f:

        return self.username == 'gua' and self.password == '123'

    def validate_register(self):
        path = os.getcwd() + '/web03/db/User.txt'
        with open(path, 'w+') as f:
            items = f.readlines()
            if
        return len(self.username) > 2 and len(self.password) > 2
