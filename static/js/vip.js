

// 更新会员状态
function updateStatus(vipId, status) {
    var statusText = status === 'active' ? '激活' : status === 'frozen' ? '冻结' : '非活跃';
    if (confirm('确定要' + statusText + '该会员吗？')) {
        fetch('/vip/update-status', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: 'vip_id=' + vipId + '&status=' + status
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert(data.message);
                // 刷新页面
                window.location.reload();
            } else {
                alert(data.message);
            }
        })
        .catch(error => {
            console.error('更新会员状态失败:', error);
            alert('更新会员状态失败，请重试');
        });
    }
}

// 删除会员
function deleteVip(vipId) {
    if (confirm('确定要删除该会员吗？')) {
        fetch('/vip/delete', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: 'vip_id=' + vipId
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert(data.message);
                // 刷新页面
                window.location.reload();
            } else {
                alert(data.message);
            }
        })
        .catch(error => {
            console.error('删除会员失败:', error);
            alert('删除会员失败，请重试');
        });
    }
}