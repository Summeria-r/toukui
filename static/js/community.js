// 获取模态框
var rejectModal = document.getElementById("rejectModal");
var detailModal = document.getElementById("detailModal");

// 获取关闭按钮
var closeBtns = document.getElementsByClassName("close");
var cancelBtns = document.getElementsByClassName("btn-cancel");

// 打开拒绝模态框的函数
function openRejectModal(postId) {
    // 填充表单数据
    document.getElementById("rejectPostId").value = postId;
    document.getElementById("rejectReason").value = "";
    
    // 显示模态框
    rejectModal.style.display = "block";
}

// 打开详情模态框的函数
function openDetailModal(postId) {
    // 发送请求获取帖子详情
    fetch(`/community/detail?post_id=${postId}`)
        .then(response => response.json())
        .then(data => {
            if (data) {
                // 填充详情数据
                document.getElementById("detailTitle").textContent = data.title;
                document.getElementById("detailUser").textContent = data.user;
                document.getElementById("detailCreateTime").textContent = data.create_time;
                document.getElementById("detailContent").textContent = data.content;
                document.getElementById("detailLikes").textContent = data.likes;
                document.getElementById("detailComments").textContent = data.comments;
                
                // 填充图片
                var imagesContainer = document.getElementById("detailImages");
                imagesContainer.innerHTML = "";
                if (data.images && data.images.length > 0) {
                    data.images.forEach(image => {
                        var img = document.createElement("img");
                        img.src = image;
                        img.className = "post-image";
                        img.alt = "帖子图片";
                        imagesContainer.appendChild(img);
                    });
                }
                
                // 显示模态框
                detailModal.style.display = "block";
            }
        })
        .catch(error => {
            console.error('获取帖子详情失败:', error);
            alert('获取帖子详情失败，请重试');
        });
}

// 关闭模态框
function closeModal(modal) {
    modal.style.display = "none";
}

// 点击关闭按钮关闭模态框
for (var i = 0; i < closeBtns.length; i++) {
    closeBtns[i].onclick = function() {
        closeModal(rejectModal);
        closeModal(detailModal);
    };
}

// 点击取消按钮关闭模态框
for (var i = 0; i < cancelBtns.length; i++) {
    cancelBtns[i].onclick = function() {
        closeModal(rejectModal);
        closeModal(detailModal);
    };
}

// 点击模态框外部关闭模态框
window.onclick = function(event) {
    if (event.target == rejectModal) {
        closeModal(rejectModal);
    }
    if (event.target == detailModal) {
        closeModal(detailModal);
    }
}

// 为批准按钮添加点击事件
function approvePost(postId) {
    if (confirm('确定要批准该帖子吗？')) {
        // 发送请求批准帖子
        fetch('/community/approve', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: 'post_id=' + postId
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // 更新页面上的状态
                var row = document.querySelector(`tr[data-post-id="${postId}"]`);
                if (row) {
                    var statusCell = row.cells[4];
                    statusCell.innerHTML = '<span class="status status-approved">已通过</span>';
                    var reviewTimeCell = row.cells[5];
                    var now = new Date();
                    var formattedTime = now.getFullYear() + '-' + 
                                        String(now.getMonth() + 1).padStart(2, '0') + '-' + 
                                        String(now.getDate()).padStart(2, '0') + ' ' + 
                                        String(now.getHours()).padStart(2, '0') + ':' + 
                                        String(now.getMinutes()).padStart(2, '0') + ':' + 
                                        String(now.getSeconds()).padStart(2, '0');
                    reviewTimeCell.textContent = formattedTime;
                    alert('帖子已成功批准');
                }
            } else {
                alert(data.message);
            }
        })
        .catch(error => {
            console.error('批准帖子失败:', error);
            alert('批准帖子失败，请重试');
        });
    }
}

// 为拒绝按钮添加点击事件
function rejectPost(postId) {
    openRejectModal(postId);
}

// 为查看详情按钮添加点击事件
function viewDetail(postId) {
    openDetailModal(postId);
}

// 提交拒绝表单
function submitRejectForm() {
    var postId = document.getElementById("rejectPostId").value;
    var rejectReason = document.getElementById("rejectReason").value;
    
    if (!rejectReason) {
        alert('请填写拒绝理由');
        return;
    }
    
    // 发送请求拒绝帖子
    fetch('/community/reject', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: 'post_id=' + postId + '&reject_reason=' + encodeURIComponent(rejectReason)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // 更新页面上的状态
            var row = document.querySelector(`tr[data-post-id="${postId}"]`);
            if (row) {
                var statusCell = row.cells[4];
                statusCell.innerHTML = '<span class="status status-rejected">已拒绝</span>';
                var reviewTimeCell = row.cells[5];
                var now = new Date();
                var formattedTime = now.getFullYear() + '-' + 
                                    String(now.getMonth() + 1).padStart(2, '0') + '-' + 
                                    String(now.getDate()).padStart(2, '0') + ' ' + 
                                    String(now.getHours()).padStart(2, '0') + ':' + 
                                    String(now.getMinutes()).padStart(2, '0') + ':' + 
                                    String(now.getSeconds()).padStart(2, '0');
                reviewTimeCell.textContent = formattedTime;
                alert('帖子已成功拒绝');
                closeModal(rejectModal);
            }
        } else {
            alert(data.message);
        }
    })
    .catch(error => {
        console.error('拒绝帖子失败:', error);
        alert('拒绝帖子失败，请重试');
    });
}

// 预设时间范围
function setTimeRange(range) {
    var now = new Date();
    var startDate, endDate;
    
    switch (range) {
        case 'today':
            startDate = now.toISOString().split('T')[0];
            endDate = startDate;
            break;
        case 'week':
            startDate = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000).toISOString().split('T')[0];
            endDate = now.toISOString().split('T')[0];
            break;
        case 'month':
            startDate = new Date(now.getFullYear(), now.getMonth(), 1).toISOString().split('T')[0];
            endDate = now.toISOString().split('T')[0];
            break;
        default:
            startDate = '';
            endDate = '';
    }
    
    document.getElementById('start_date').value = startDate;
    document.getElementById('end_date').value = endDate;
}