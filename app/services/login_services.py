from app.models.userinfo import UserInfo
from app.security import verify_password  # 记得加这个
from app.exceptions import (
    InvalidParameterException,
    UserNotExistsException,
    PasswordErrorException
)

async def login_user(account: str, password: str) -> UserInfo:
    # 1. 参数校验
    if not account or not password:
        raise InvalidParameterException(detail="账号和密码不能为空")

    # 2. 查询用户是否存在
    user = await UserInfo.filter(account=account).first()
    
    if not user:
        raise UserNotExistsException(detail="账号不存在，请先注册！")
    

    # 3. 校验密码
    if not verify_password(password, user.password):
        raise PasswordErrorException(detail="密码错误，请重新输入！")

    # 4. 登录成功，返回用户
    return user