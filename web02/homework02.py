# 2017/02/18
# 作业 2
# ========
#
#
# 请直接在我的代码中更改/添加, 不要新建别的文件

import re
from web01.homework01 import get
import time


# 定义我们的 log 函数
def log(*args, **kwargs):
    print(*args, **kwargs)


# 作业 2.1
#
# 实现函数
def path_with_query(path, query):
    '''
    path 是一个字符串
    query 是一个字典

    返回一个拼接后的 url
    详情请看下方测试函数
    '''
    query_str = ''
    for q in query:
        value = str(q) + '=' + str(query[q]) + '&'
        log(value)
        query_str += value
    return path + '?' + query_str[:-1]


# def test_path_with_query():
#     path = '/'
#     query = {
#         'name': 'gua',
#         'height': 169,
#     }
#     expected = [
#         '/?name=gua&height=169',
#         '/?height=169&name=gua',
#     ]
#     assert path_with_query(path, query) in expected


# 作业 2.2
#
# 为作业1 的 get 函数增加一个参数 query
# query 是字典


# 作业 2.3
#
# 实现函数
def header_from_dict(headers):
    '''
    headers 是一个字典
    范例如下
    对于
    {
      'Content-Type': 'text/html',
      'Content-Length': 127,
    }
    返回如下 str
    'Content-Type: text/html\r\nContent-Length: 127\r\n'
    '''
    headers_str = ''
    for h in headers:
        headers_str += str(h) + ': ' + str(headers[h]) + '\r\n'
    print(headers_str)
    return headers_str


# 作业 2.4
#
# 为作业 2.3 写测试
# def test_header_from_dict():
#     headers = {
#         'Connection': 'Keep-Alive', 'Content-Type': 'text/html',
#     }
#     respected = [
#         'Connection: Keep-Alive\r\nContent-Type: text/html\r\n',
#         'Content-Type: text/html\r\nConnection: Keep-Alive\r\n',
#     ]
#     assert header_from_dict(headers) in respected


# 作业 2.5
#
"""
豆瓣电影 Top250 页面链接如下
https://movie.douban.com/top250
我们的 client_ssl.py 已经可以获取 https 的内容了
这页一共有 25 个条目

所以现在的程序就只剩下了解析 HTML

请观察页面的规律，解析出
1，电影名
2，分数
3，评价人数
4，引用语（比如第一部肖申克的救赎中的「希望让人自由。」）

解析方式可以用任意手段，如果你没有想法，用字符串查找匹配比较好(find 特征字符串加切片)
"""


def crawl_douban(url, query):
    status_code, headers, body = get(url, query)

    pattern = re.compile('<li>(.*?)</li>', re.S)
    all_items = pattern.findall(body)
    for i in all_items:
        # 电影名
        titles = ''
        # 电影评分
        score = ''
        # 评价人数
        people_count = ''
        # 引用语
        comments = ''
        try:
            title_item = i.split('span')
            for t in title_item:
                titles += t.split('class="title">')[1].split('<')[0].strip().replace('&nbsp;', '').replace('/',
                                                                                                           '') + ';' if 'title' in t else ''
                titles += t.split('class="other">')[1].split('<')[0].strip().replace('&nbsp;', '').replace('/',
                                                                                                           '') + ';' if 'other' in t else ''
                if 'rating_num' in t:
                    score = t.split('property="v:average">')[1].split('<')[0].strip()
                if '人评价' in t:
                    people_count = t.split('>')[1].split('<')[0].strip()[:-3]
                if 'inq' in t:
                    comments = t.split('>')[1].split('<')[0].strip()


        except Exception as e:
            print('no title, {}'.format(e))
        if titles:
            print('titles: {}'.format(titles))
            print('score: {} 分'.format(score))
            print('people_count: {} 人评价'.format(people_count))
            print('comments: {}'.format(comments))
            print('\n')


# 作业 2.6
#
"""
通过在浏览器页面中访问 豆瓣电影 top250 可以发现
1, 每页 25 个条目
2, 下一页的 URL 如下
https://movie.douban.com/top250?start=25

因此可以用循环爬出豆瓣 top250 的所有网页

于是就有了豆瓣电影 top250 的所有网页

由于这 10 个页面都是一样的结构，所以我们只要能解析其中一个页面就能循环得到所有信息

所以现在的程序就只剩下了解析 HTML

请观察规律，解析出
1，电影名
2，分数
3，评价人数
4，引用语（比如第一部肖申克的救赎中的「希望让人自由。」）

解析方式可以用任意手段，如果你没有想法，用字符串查找匹配比较好(find 特征字符串加切片)
"""


def crawl_top250_douban():
    for i in range(10):
        log('打印第{}页的电影信息'.format(i))
        query = {
            'start': i * 25
        }
        url = 'https://movie.douban.com/top250'
        crawl_douban(url, query)
        log('打印第{}页的电影信息完成，5s后继续'.format(i + 1))
        time.sleep(5)


if __name__ == '__main__':
    crawl_top250_douban()
