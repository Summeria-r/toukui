console.log("管理后台 JS 加载成功")

// 示例：给按钮加点击事件
document.addEventListener('DOMContentLoaded', function() {
    const btns = document.querySelectorAll('.btn')
    btns.forEach(btn => {
        btn.addEventListener('click', function() {
            console.log("点击按钮：", this.textContent.trim())
        })
    })
})

// 可以在这里写：
// 搜索、弹窗、表单提交、AJAX 请求等