from utils import log
from models import Message
from models import User

import random


# 这个函数用来保存所有的 messages
message_list = []
session = {}


def random_str():
    """
    生成一个随机的字符串
    """
    seed = 'abcdefjsad89234hdsfkljasdkjghigaksldf89weru'
    s = ''
    for i in range(16):
        random_index = random.randint(0, len(seed) - 2)
        s += seed[random_index]
    return s


if __name__ == '__main__':
    print(random_str())