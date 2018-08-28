var timeString = function(timestamp){
    t = new Date(timestamp * 1000)
    t = t.toLocaleTimeString()
    return t
}


var commentsTempalte = function(comments){
    var html = ''
    for (var i = 0; i< comments.length; i++){
        var c = comments[i]
        var t = `
            <div>
                ${c.content}
            </div>
        `
        html += t
    }
    return html
}

var weiboTemplate = function(weibo) {
    var content = weibo.content
    var id = weibo.id
    var comments = commentsTempalte(weibo.comments)
    // data-xx 是自定义标签的语法
    // 假设d是这个div的引用
    // 这样的自定义属性通过 d.dataset.xx 来获取
    // 在这个例子里面,是d.dataset.id

    var t = `
        <div class= 'weibo-cell' data-id=${id}>
            <div>
                ${content}
            </div>
            <div class='comment-list'>
                ${comments}
            </div>
            <div class="comment-form">
                <input type="hidden" name="weibo_id" value="">
                <input name="content">
                <br>
                <button class="comment-add">添加评论</button>
            </div>
        </div>
    `
    return t
}

var insertWeibo = function(weibo) {
    var weiboCell = weiboTemplate(weibo)
    // 插入 weibo-list
    var weiboList = e('.weibo-list')
    weiboList.insertAdjacentHTML('beforeend', weiboCell)
}

var insertEditForm = function(cell){
    var form = `
        <div class='todo-edit-form'>
            <input class="todo-edit-input">
            <button class='todo-update'>更新</button>
        </div>
    `
    cell.insertAdjacentHTML('beforeend', form)
}

var loadWeibos = function() {
    // 调用 ajax api 来载入数据
    apiWeiboAll(function(r) {
        // console.log('load all', r)
        // 解析为 数组
        var todos = JSON.parse(r)
        // 循环添加到页面中
        for(var i = 0; i < todos.length; i++) {
            var todo = todos[i]
            insertWeibo(todo)
        }
    })
}

var bindEventWeiboAdd = function() {
    var b = e('.comment-add')
    // 注意, 第二个参数可以直接给出定义函数
    b.addEventListener('click', function(){
        var input = e('#id-input-todo')
        var title = input.value
        log('click add', title)
        var form = {
            title: title,
        }
        apiWeiboAdd(form, function(r) {
            // 收到返回的数据, 插入到页面中
            var todo = JSON.parse(r)
            insertWeibo(todo)
        })
    })
}

var bindEventWeiboDelete = function() {
    var b = e('.todo-list')
    // 注意, 第二个参数可以直接给出定义函数
    b.addEventListener('click', function(event){
        var self =event.target
        if(self.classList.contains('todo-delete')){
            // 删除这个TODO
            var todoCell = self.parentElement
            var todo_id = todoCell.dataset.id
            apiWeiboDelete(todo_id, function(r){
                log('删除成功', todo_id)
                todoCell.remove()
            })
        }
    })
}


var bindEventWeiboEdit = function() {
    var b = e('.todo-list')
    // 注意, 第二个参数可以直接给出定义函数
    b.addEventListener('click', function(event){
        var self =event.target
        if(self.classList.contains('todo-edit')){
            // 删除这个TODO
            var todoCell = self.parentElement
            insertEditForm(todoCell)
        }
    })
}

var bindEventWeiboUpdate = function() {
    var b = e('.todo-list')
    // 注意, 第二个参数可以直接给出定义函数
    b.addEventListener('click', function(event){
        var self =event.target
        if(self.classList.contains('todo-update')){
            log('点击了update')
            // 更新这个TODO
            var editForm = self.parentElement
            var input = editForm.querySelector('.todo-edit-input')
            var todoCell = self.closest('.todo-cell')
            var todo_id = todoCell.dataset.id
            var title = input.value
            var form = {
                'id': todo_id,
                'title': title,
            }
            apiWeiboUpdate(form, function(r){
                log('更新成功', todo_id)
                var todo = JSON.parse(r)
                var selector = '#todo-' + todo.id
                var todoCell = e(selector)
                var titleSpan = todoCell.querySelector('.todo-title')
                titleSpan.innerHTML = todo.title
            })

        }
    })
}

var bindEvents = function() {
    bindEventWeiboAdd()
//    bindEventWeiboDelete()
//    bindEventWeiboEdit()
//    bindEventWeiboUpdate()
}


var __main = function() {
    bindEvents()
    loadWeibos()
}

__main()