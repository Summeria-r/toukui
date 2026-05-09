# 存放所有和身份认证、权限校验、安全相关的通用逻辑
from fastapi import HTTPException, Request
from app.models.userinfo import UserInfo


#验证密码
def verify_password(plain_password: str, stored_password: str) -> bool:
    """
    plain_password: 用户输入的明文密码
    stored_password: 数据库中存储的明文密码
    """
    return plain_password == stored_password


async def change_password(user, old_password: str, new_password: str) -> bool:
    """更改用户密码
    
    Args:
        user: 用户对象
        old_password: 旧密码
        new_password: 新密码
    
    Returns:
        bool: 密码更改是否成功
    
    Raises:
        HTTPException: 旧密码错误时抛出
    """
    # 验证旧密码
    if not verify_password(old_password, user.password):
        raise HTTPException(status_code=400, detail="旧密码错误")
    
    
    # 保存更改到数据库
    await user.save()
    
    return True


#=================用户认证=========================

async def get_current_user(request: Request):
    """从Session中获取当前登录用户，未登录则抛出401"""
    user_info = request.session.get("user")
    if not user_info:
        raise HTTPException(status_code=401, detail="请先登录")
    # 从数据库查询完整用户信息（可选，根据需求）
    user = await UserInfo.get_or_none(id=user_info["id"])
    if not user:
        raise HTTPException(status_code=401, detail="用户不存在，请重新登录")
    return user

async def save_user_session(request: Request, user) -> None:
    
    user_data = {
        "id": user.id,
        "account": user.account
    }
    request.session["user"] = user_data
    

async def delete_user_session(request: Request) -> None:
    """删除用户会话
    
    Args:
        request: FastAPI请求对象
    """
    # 从会话中移除用户信息
    request.session.pop("user", None)

"""1.request.session["user_id"] = user.id
2.request.session.get("user_id")
3.request.session.pop("user_id", None)"""

# 注意：get_current_user函数中使用的是request.session.get("user")，与save_user_session保持一致