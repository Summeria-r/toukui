// 获取模态框
var createModal = document.getElementById("createModal");
var editModal = document.getElementById("editModal");

// 获取按钮
var createBtn = document.getElementById("createBtn");
var closeBtns = document.getElementsByClassName("close");
var cancelBtns = document.getElementsByClassName("btn-cancel");

// 打开创建商品模态框
function openCreateModal() {
    document.getElementById("createForm").reset();
    createModal.style.display = "block";
}

// 打开编辑商品模态框
function openEditModal(productId) {
    // 发送请求获取商品信息
    fetch(`/product/detail?product_id=${productId}`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                var product = data.product;
                document.getElementById("editProductId").value = product.id;
                document.getElementById("editName").value = product.name;
                document.getElementById("editPrice").value = product.price;
                document.getElementById("editTotalCount").value = product.total_count;
                document.getElementById("editSoldCount").value = product.sold_count;
                document.getElementById("editCategory").value = product.category;
                document.getElementById("editStatus").value = product.status;
                editModal.style.display = "block";
            } else {
                alert(data.message);
            }
        })
        .catch(error => {
            console.error('获取商品信息失败:', error);
            alert('获取商品信息失败，请重试');
        });
}

// 关闭模态框
function closeModal(modal) {
    modal.style.display = "none";
}

// 点击关闭按钮关闭模态框
for (var i = 0; i < closeBtns.length; i++) {
    closeBtns[i].onclick = function() {
        closeModal(createModal);
        closeModal(editModal);
    };
}

// 点击取消按钮关闭模态框
for (var i = 0; i < cancelBtns.length; i++) {
    cancelBtns[i].onclick = function() {
        closeModal(createModal);
        closeModal(editModal);
    };
}

// 点击模态框外部关闭模态框
window.onclick = function(event) {
    if (event.target == createModal) {
        closeModal(createModal);
    }
    if (event.target == editModal) {
        closeModal(editModal);
    }
}

// 提交创建商品表单
function submitCreateForm() {
    var form = document.getElementById("createForm");
    var formData = new FormData(form);
    
    fetch('/product/create', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert(data.message);
            closeModal(createModal);
            // 刷新页面
            window.location.reload();
        } else {
            alert(data.message);
        }
    })
    .catch(error => {
        console.error('创建商品失败:', error);
        alert('创建商品失败，请重试');
    });
    
    return false;
}

// 提交编辑商品表单
function submitEditForm() {
    var form = document.getElementById("editForm");
    var formData = new FormData(form);
    
    fetch('/product/update', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert(data.message);
            closeModal(editModal);
            // 刷新页面
            window.location.reload();
        } else {
            alert(data.message);
        }
    })
    .catch(error => {
        console.error('更新商品失败:', error);
        alert('更新商品失败，请重试');
    });
    
    return false;
}

// 删除商品
function deleteProduct(productId) {
    if (confirm('确定要删除该商品吗？')) {
        fetch('/product/delete', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: 'product_id=' + productId
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
            console.error('删除商品失败:', error);
            alert('删除商品失败，请重试');
        });
    }
}

// 切换商品状态
function toggleStatus(productId) {
    fetch('/product/toggle-status', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: 'product_id=' + productId
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
        console.error('切换商品状态失败:', error);
        alert('切换商品状态失败，请重试');
    });
}

// 排序功能
function sortBy(column) {
    var currentSortBy = document.getElementById('sort_by').value;
    var currentSortOrder = document.getElementById('sort_order').value;
    
    var newSortOrder = 'asc';
    if (currentSortBy == column && currentSortOrder == 'asc') {
        newSortOrder = 'desc';
    }
    
    document.getElementById('sort_by').value = column;
    document.getElementById('sort_order').value = newSortOrder;
    document.getElementById('searchForm').submit();
}

// 双击编辑功能
function enableEdit(cell, productId, field) {
    var originalValue = cell.textContent;
    var input = document.createElement('input');
    input.type = field === 'price' ? 'number' : 'text';
    input.value = originalValue;
    input.style.width = '100%';
    
    cell.innerHTML = '';
    cell.appendChild(input);
    input.focus();
    
    input.addEventListener('blur', function() {
        var newValue = input.value;
        if (newValue !== originalValue) {
            updateProductField(productId, field, newValue);
        }
        cell.textContent = newValue;
    });
    
    input.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            var newValue = input.value;
            if (newValue !== originalValue) {
                updateProductField(productId, field, newValue);
            }
            cell.textContent = newValue;
        }
    });
}

// 更新商品字段
function updateProductField(productId, field, value) {
    fetch('/product/update', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: 'product_id=' + productId + '&' + field + '=' + value
    })
    .then(response => response.json())
    .then(data => {
        if (!data.success) {
            alert(data.message);
        }
    })
    .catch(error => {
        console.error('更新商品字段失败:', error);
        alert('更新商品字段失败，请重试');
    });
}