from rest_framework import serializers
from goods.models import SPUSpecification, SKUImage, SKU


class SPUSpecificationSerializer(serializers.ModelSerializer):
    """spu序列化器"""
    # 关联查询
    spu = serializers.StringRelatedField()
    spu_id = serializers.IntegerField()

    class Meta:
        model = SPUSpecification
        fields = ('id', 'name', 'spu', 'spu_id')


class SPUSpecificationSimpleSerializer(serializers.ModelSerializer):
    """spu序列化器(simple)"""

    class Meta:
        model = SPUSpecification
        fields = ('id', 'name')


class ImageSerializer(serializers.ModelSerializer):
    """SKU图片序列化器"""

    class Meta:
        model = SKUImage
        fields = ('id', 'sku', 'image')


class ImageSimpleSerializer(serializers.ModelSerializer):
    """SKU信息序列化器(simple)"""

    class Meta:
        model = SKU
        fields = ('id', 'name',)
