'''
链表练习
'''


class Node:
    def __init__(self, element=None):
        self.e = element
        self.next = None


def append(node, element):
    '''
    在最后添加一个元素
    '''
    n = node
    while n.next is not None:
        n = n.next
        # n 现在是最后一个元素
    new_node = Node(element)
    n.next = new_node


def prepend(head, element):
    '''
    插入到链表头
    '''
    n = Node(element)
    n.next = head.next
    head.next = n


def pop(head):
    '''
    pop 是 stack 的两个操作之一
    push 入栈
    pop 出栈

    '''
    tail = head
    while tail.next is not None:
        tail = tail.next
        # tail 是最后一个元素了
    n = head
    while n.next is not tail:
        n = n.next
        # n 是tail 之前的元素
    n.next = None
    return tail.e
