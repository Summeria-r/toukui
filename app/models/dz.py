from tortoise import Model, fields

class Dz(Model):
    """车友圈点赞表"""
    # 点赞用户ID（关联 userinfo.id）
    # 注意：数据库里没有自增，所以不要写 pk=True 也不要写 auto_increment
    id = fields.IntField(pk=True, description="点赞用户ID（关联userinfo.id）")
    
    # 关联作品ID（关联 zptable.id）
    zpid = fields.IntField(description="关联zptable.id")

    class Meta:
        table = "dz"
        description = "车友圈点赞表"
        # 声明联合主键
        composite_pk = True
        # 指定联合主键的字段顺序
        unique_together = ("id", "zpid")