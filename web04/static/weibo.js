// 时间转换工具
var timeString = function(timestamp){
    t = new Date(timestamp * 1000)
    t = t.toLocaleTimeString()
    return t
}

// 评论模版
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

// 微博模版
var weiboTemplate = function(weibo) {
    var content = weibo.content
    var id = weibo.id
    var comments = commentsTempalte(weibo.comments)
    // data-xx 是自定义标签的语法
    // 假设d是这个div的引用
    // 这样的自定义属性通过 d.dataset.xx 来获取
    // 在这个例子里面,是d.dataset.id

    var t = `
        <div class='weibo-cell' data-id=${id}>
            <hr>
            <div class='weibo-content'>
                [微博内容] ${content}
            </div>
            <button class="weibo-delete">删除微博</button>
            <button class="weibo-edit">编辑微博</button>
            <div class='comment-list'>
                [微博评论] ${comments}
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

// 清空输入框
var clearFrom = function(element) {
    var form = e(element)
    log('输入框的元素 ', element)
    log('输入框的值 ', form.value)
    form.innerHTML = ''
    log('已清空输入框')
}

// 插入微博
var insertWeibo = function(weibo) {
    var weiboCell = weiboTemplate(weibo)
    // 插入 weibo-list
    var weiboList = e('.weibo-list')
    weiboList.insertAdjacentHTML('beforeend', weiboCell)
}

// 插入输入框
var insertEditForm = function(cell){
    var form = `
        <div class='weibo-edit-form'>
            <input class="weibo-edit-input">
            <button class='weibo-update'>更新</button>
        </div>
    `
    cell.insertAdjacentHTML('afterend', form)
}

// 载入微博数据
var loadWeibos = function() {
    // 调用 ajax api 来载入数据
    apiWeiboAll(function(r) {
         console.log('load all', r)
        // 解析为 数组
        var weibos = JSON.parse(r)
        // 循环添加到页面中
        for(var i = 0; i < weibos.length; i++) {
            var weibo = weibos[i]
            insertWeibo(weibo)
        }
        clearFrom('#id-input-weibo')
    })
}

// 绑定微博添加事件
var bindEventWeiboAdd = function() {
    var b = e('#id-button-add-weibo')
    // 注意, 第二个参数可以直接给出定义函数
    b.addEventListener('click', function(){
        var input = e('#id-input-weibo')
        var weibo_content = input.value
        log('微博内容: ', weibo_content)
        var form = {
            content: weibo_content,
        }
        apiWeiboAdd(form, function(r) {
            // 收到返回的数据, 插入到页面中
            var weibo = JSON.parse(r)
            insertWeibo(weibo)
        })
    })
}

// 绑定微博删除事件
var bindEventWeiboDelete = function() {
    var b = e('.weibo-list')
    // 注意, 第二个参数可以直接给出定义函数
    b.addEventListener('click', function(event){
        var self = event.target
        if(self.classList.contains('weibo-delete')){
            // 删除这个TODO
            log('点击了删除按钮')
            var weiboCell = self.parentElement
            var weibo_id = weiboCell.dataset.id
            form = {
                'weibo_id': weibo_id
            }
            apiWeiboDelete(form, function(r){
                log('删除成功', weibo_id)
                weiboCell.remove()
            })
        }
    })
}

// 绑定微博编辑事件
var bindEventWeiboEdit = function() {
    var b = e('.weibo-list')
    // 注意, 第二个参数可以直接给出定义函数
    b.addEventListener('click', function(event){
        var self =event.target
        if(self.classList.contains('weibo-edit')){
            // 编辑这个weibo
            var weiboCell = self.parentElement
            // 获取微博内容的element, 删除后插入一个表单，里面有 weibo 内容和 update 按钮
            var weiboConent = weiboCell.children[1]
//            log('weiboConent', weiboConent)
//            log('weiboCell', weiboCell)
            insertEditForm(weiboConent)
            weiboConent.remove()
        }
    })
}

// 绑定微博更新事件
var bindEventWeiboUpdate = function() {
    var b = e('.weibo-list')
    // 注意, 第二个参数可以直接给出定义函数
    b.addEventListener('click', function(event){
        var self =event.target
        if(self.classList.contains("weibo-update")){
            log('点击了update')
            // 更新这个TODO
            var editForm = self.parentElement
            var input = editForm.querySelector('.weibo-edit-input')
            var weiboCell = self.closest('.weibo-cell')
            var weibo_id = weiboCell.dataset.id
            var weibo_content = input.value
            var form = {
                'id': weibo_id,
                'content': weibo_content,
            }
            apiWeiboUpdate(form, function(r){
                log('更新成功', weibo_id)
                loadWeibos()
//                var weibo = JSON.parse(r)
//                var selector = '#weibo-' + weibo.id
//                var weiboCell = e(selector)
//                var titleSpan = todoCell.querySelector('.todo-title')
//                titleSpan.innerHTML = todo.title
            })

        }
    })
}

// 事件绑定区
var bindEvents = function() {
    bindEventWeiboAdd()
    bindEventWeiboDelete()
    bindEventWeiboEdit()
    bindEventWeiboUpdate()
}

// 程序的主入口
var __main = function() {
    bindEvents()
    loadWeibos()
}

// 调用主入口
__main()