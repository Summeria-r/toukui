from tortoise import Model, fields

class Product(Model):
    """商品模型"""
    id = fields.IntField(pk=True, index=True, description="商品ID")
    name = fields.CharField(max_length=255, description="商品名称")
    price = fields.FloatField(description="商品价格")
    image = fields.CharField(max_length=255, null=True, description="商品图片")
    total_count = fields.IntField(default=0, null=True, description="总数量")
    sold_count = fields.IntField(default=0, null=True, description="卖出数量")
    category = fields.CharField(max_length=50, null=True, description="商品分类")
    status = fields.CharField(
        max_length=10, 
        default="on_sale", 
        description="商品状态：on_sale上架 / off_sale下架 / sold_out售罄"
    )
    class Meta:
        table = "product"
        description = "商品表"