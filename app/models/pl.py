from tortoise import Model, fields

class Pl(Model):
    """评论表"""
    id = fields.IntField(pk=True, description="主键ID")
    zpid = fields.IntField(index=True, description="作品ID")
    userid = fields.IntField(description="用户ID")
    content = fields.CharField(max_length=500, description="评论内容")
    time = fields.DatetimeField(description="评论时间")

    class Meta:
        table = "pl"
