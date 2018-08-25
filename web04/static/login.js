// 集成方法
var e = function(sel) {
    return document.querySelector(sel)
}

var log = function() {
    console.log.apply(console, arguments)
}

var inform_template = function(value){
    var t = `
    <h3>${value}</h3>
    `
    return t
}

// 添加tag
var append_tag = function(value){
    var inform_tag = inform_template(value)
    // 插入 inform_tag
    var body = e('body')
    body.insertAdjacentHTML('beforeend', inform_tag)
}

// 获取button的dom
var submit_btn = e('#login-button')
submit_btn.addEventListener('click', function(){
    log('login click')
    var input = e('#user-input')
    var value = input.value
    first_str = value.slice(0, 1)
    str_length = value.length
    last_str = value.slice(str_length-1)
    log('第一个字符: ', first_str)
    log('字符长度: ', str_length)
    log('最后一个字符: ', last_str)
    if (/^[A-Za-z0-9_]*$/.test(value) && /^[A-Za-z0-9]*$/.test(last_str) && value.length <= 10){
        append_tag('检查合格')
    }
    else{
        append_tag('用户名错误')

        // 清空用户输入的内容
        var clear_input = function(){
            var input = e('#user-input')
            var input_value = input.value
            log('user input', input_value)
            input.value = ''
        }
        clear_input()
    }
})

