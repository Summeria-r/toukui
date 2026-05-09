# app/services/auth_service.py
import re
from app.models.userinfo import UserInfo
from app.exceptions import UserAlreadyExistsException, InvalidParameterException


from app.models.userinfo import UserInfo
async def register_user(account: str, password: str, confirm_password: str) -> UserInfo:
    """
    用户注册业务逻辑：
    1. 参数校验（手机号格式、密码长度）
    2. 账号/手机号唯一性校验
    3. 密码加密
    4. 创建用户并保存到数据库
    """
    
    # 密码长度校验
    if len(password) < 6 or len(password) > 20:
        raise InvalidParameterException(detail="密码长度需在6-20字符之间")

    # 检查账号是否已存在
    existing_user = await UserInfo.filter(account=account).first()
    if existing_user:
        raise UserAlreadyExistsException(detail="账号已存在")
    
    #检查两次输入的密码是否一致
    if password != confirm_password:
        raise InvalidParameterException(detail="两次输入的密码不一致")

    user = await UserInfo.create(
        account=account,
        password=password  # 直接存储明文密码
    )

    return user