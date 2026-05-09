// 获取模态框
var modal = document.getElementById("editModal");

// 获取关闭按钮
var closeBtn = document.getElementsByClassName("close")[0];
var cancelBtn = document.getElementsByClassName("btn-cancel")[0];

// 打开模态框的函数
function openEditModal(userId, account, password, status) {
    // 填充表单数据
    document.getElementById("userId").value = userId;
    document.getElementById("editAccount").value = account;
    document.getElementById("editPassword").value = password;
    document.getElementById("editStatus").value = status;
    
    // 显示模态框
    modal.style.display = "block";
}

// 关闭模态框
function closeModal() {
    modal.style.display = "none";
}

// 点击关闭按钮关闭模态框
closeBtn.onclick = closeModal;
cancelBtn.onclick = closeModal;

// 点击模态框外部关闭模态框
window.onclick = function(event) {
    if (event.target == modal) {
        closeModal();
    }
}

// 为编辑按钮添加点击事件
document.addEventListener('DOMContentLoaded', function() {
    var editButtons = document.getElementsByClassName('btn-edit');
    for (var i = 0; i < editButtons.length; i++) {
        editButtons[i].onclick = function() {
            // 获取用户信息
            var row = this.closest('tr');
            var userId = row.cells[0].textContent;
            var account = row.cells[1].textContent;
            var password = row.cells[2].textContent;
            var status = row.cells[5].textContent.trim();
            
            // 转换状态值
            if (status === '正常') {
                status = '0';
            } else if (status === '禁用') {
                status = '1';
            }
            
            // 打开模态框
            openEditModal(userId, account, password, status);
        };
    }
    
    // 为禁用按钮添加点击事件
    var disableButtons = document.getElementsByClassName('btn-disable');
    for (var i = 0; i < disableButtons.length; i++) {
        disableButtons[i].onclick = function() {
            // 获取用户信息
            var row = this.closest('tr');
            var userId = row.cells[0].textContent;
            var statusCell = row.cells[5];
            var statusText = statusCell.textContent.trim();
            
            // 确认是否禁用用户
            if (confirm('确定要禁用该用户吗？')) {
                // 发送请求禁用用户
                fetch('/user/disable', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded'
                    },
                    body: 'user_id=' + userId
                })
                .then(response => response.text())
                .then(data => {
                    // 更新页面上的状态
                    statusCell.innerHTML = '<span class="status status-disabled">禁用</span>';
                    alert('用户已成功禁用');
                })
                .catch(error => {
                    console.error('禁用用户失败:', error);
                    alert('禁用用户失败，请重试');
                });
            }
        };
    }
});