from tortoise import Model, fields


class UserInfo(Model):
    id = fields.IntField(pk=True, index=True)
    account = fields.CharField(max_length=50, unique=True, index=True, description="用户账号")
    username = fields.CharField(max_length=50, null=True, description="用户名")
    usertx = fields.BinaryField(null=True, description="用户头像（二进制）")
    password = fields.CharField(max_length=100, description="密码哈希值")
    openid = fields.CharField(max_length=100, null=True, description="微信openid")
    create_time = fields.DatetimeField(auto_now_add=True, null=True, description="创建时间")
    update_time = fields.DatetimeField(auto_now=True, null=True, description="更新时间")
    status = fields.CharField(max_length=10, default="0", description="用户状态")

    class Meta:
        table = "userinfo"
        description = "用户表"