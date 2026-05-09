from tortoise import Model, fields

class ZpTable(Model):
    """车友圈作品表"""
    id = fields.IntField(pk=True, description="主键ID")
    userid = fields.IntField(index=True, description="用户ID")
    zptitle = fields.CharField(max_length=255)
    zpcontent = fields.TextField()
    zpimg = fields.BinaryField(null=True)
    zpsj = fields.DatetimeField()
    zpdz = fields.IntField(default=0)
    pl = fields.IntField(default=0)
    status = fields.CharField(
        max_length=10, 
        default="pending", 
        description="审核状态：pending待审核 / approved已通过 / rejected已拒绝"
    )
    reject_reason = fields.CharField(
        max_length=255, 
        null=True, 
        default=None,
        description="拒绝原因"
    )
    audit_time = fields.DatetimeField(null=True, description="审核时间")



    class Meta:
        table = "zptable"
        indexes = [
            ("status",),
        ]