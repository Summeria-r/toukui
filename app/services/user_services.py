from app.models.userinfo import UserInfo
from typing import List, Dict, Optional
from fastapi import Query
import pandas as pd
from tortoise.expressions import Q
from io import BytesIO

async def get_user_list(
    page: int = 1,
    page_size: int = 10,
    search: Optional[str] = None,
    status: Optional[str] = None
) -> Dict:
    """获取用户列表"""
    # 构建查询
    query = UserInfo.all()
    
    # 搜索条件
    if search:
        # 尝试将搜索关键词转换为整数，用于ID搜索
        try:
            search_id = int(search)
            # 用 Q 对象实现 AND/OR 查询
            query = query.filter(
                Q(id=search_id) | Q(account__contains=search)
            )
        except ValueError:
            # 如果不是数字，则只搜索账号
            query = query.filter(
                Q(account__contains=search)
            )
    
    # 状态筛选
    if status:
        # 根据实际的状态字段来筛选
        # 转换状态值，前端使用"正常"和"禁用"，模型中使用"0"和"1"
        status_map = {
            "正常": "0",
            "禁用": "1"
        }
        status_value = status_map.get(status, status)
        query = query.filter(
            Q(status=status_value)
        )
    
    # 计算总数
    total = await query.count()
    
    # 分页
    users = await query.offset((page - 1) * page_size).limit(page_size).all()
    
    # 构建返回结果
    result = {
        "users": users,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": (total + page_size - 1) // page_size
    }
    
    return result

async def export_users_to_excel() -> BytesIO:
    """导出用户数据到Excel"""
    # 获取所有用户
    users = await UserInfo.all()
    
    # 构建数据
    data = []
    for user in users:
        # 转换状态值，模型中使用"0"和"1"，显示为"正常"和"禁用"
        status_map = {
            "0": "正常",
            "1": "禁用"
        }
        status_text = status_map.get(user.status, user.status)
        data.append({
            "ID": user.id,
            "账号": user.account,
            "注册时间": user.create_time.strftime("%Y-%m-%d %H:%M:%S") if user.create_time else "",
            "最后登录时间": user.update_time.strftime("%Y-%m-%d %H:%M:%S") if user.update_time else "",
            "用户状态": status_text
        })
    
    # 创建DataFrame
    df = pd.DataFrame(data)
    
    # 导出到Excel
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='用户列表', index=False)
    
    output.seek(0)
    return output

async def update_user_status(user_id: int, status: str) -> bool:
    """更新用户状态"""
    user = await UserInfo.get_or_none(id=user_id)
    if not user:
        return False
    
    # 转换状态值，前端使用"正常"和"禁用"，模型中使用"0"和"1"
    status_map = {
        "正常": "0",
        "禁用": "1"
    }
    status_value = status_map.get(status, status)
    
    # 更新用户状态
    user.status = status_value
    await user.save()
    
    return True

async def update_user(user_id: int, account: str, password: str, status: str) -> bool:
    """更新用户信息"""
    user = await UserInfo.get_or_none(id=user_id)
    if not user:
        return False
    
    # 更新用户信息
    user.account = account
    user.status = status
    
    # 如果密码不为空，则更新密码
    if password:
        user.password = password
    
    await user.save()
    
    return True