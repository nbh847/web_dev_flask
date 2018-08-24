/*
1, 给 add button 绑定事件
2, 在事件处理函数中，获取 input 的值
3，用获取的值组装一个todo-cell 并插入todo-list 中
*/
var log = function(){
    console.log.apply(console, arguments)
}

var e = function(sel){
    return document.querySelector(sel)
}

var todotemplate = function(todo) {
    var t =`
        <div class="todo-cell">
            <button class="todo-delete">删除</button>
            <span>${todo}</span>
        </div>
    `
    return t
}

var insertTodo = function(todo) {
    // 插入todo-list
    var todoList = e('.todo-list')
    var todoCell = todotemplate(todo)
    todoList.insertAdjacentHTML('beforeend', todoCell)
}

var b = e('#id-button-add')

// 第二个参数可直接给出定义函数
b.addEventListener('click', function() {
    var input = e('#id-input-todo')
    var todo = input.value
    log('todo', todo)
    insertTodo(todo)
})

/*
给 删除 按钮绑定删除事件
1, 绑定事件
2，删除整个todo-cell 元素
*/
var todoList = e('.todo-list')
// 事件响应函数会被传入一个参数，就是事件本身
todoList.addEventListener('click', function(event){
//    log('todo list click', event)
    // 我们可以通过event.target 来得到被点击的对象
    var self = event.target
//    log('被点击的元素', self)
    // classList 属性保存了元素的所有class
//    log(self.classList)
    if (self.classList.contains('todo-delete')){
        log('点到了删除按钮')
        // 删除 self 的父节点
        self.parentElement.remove()
    }
    else{
//        log('没有点到删除按钮')
    }
})