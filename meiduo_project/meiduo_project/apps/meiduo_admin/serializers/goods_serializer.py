from rest_framework import serializers

from goods.models import GoodsVisitCount


class GoodsSerializer(serializers.ModelSerializer):
    # 指定返回字段的str方法分类名称
    category = serializers.StringRelatedField(read_only=True)

    class Meta:
        # 指定模型
        model = GoodsVisitCount
        # 指定返回字段
        fields = ('count', 'category')
        
        



