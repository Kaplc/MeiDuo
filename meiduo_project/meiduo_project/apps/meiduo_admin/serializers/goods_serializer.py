from django.conf import settings
from fdfs_client.client import Fdfs_client
from rest_framework import serializers
from goods.models import SPUSpecification, SpecificationOption, SPU, Brand, GoodsCategory, GoodsChannel, \
    GoodsChannelGroup


# ------------------------------------------ #
class GoodsChannelSerializer(serializers.ModelSerializer):
    """
        meiduo_admin/goods/channels
        频道管理
    """
    category = serializers.StringRelatedField()
    category_id = serializers.IntegerField()
    group_id = serializers.IntegerField()
    group = serializers.StringRelatedField()

    class Meta:
        model = GoodsChannel
        fields = ('id', 'category', 'sequence', 'url', 'group', 'group_id', 'category_id',)
        #

    # ------------------------------------------ #


class SPUSpecificationSerializer(serializers.ModelSerializer):
    """

        规格管理SPUSpecification序列化器
    """
    # 关联查询
    spu = serializers.StringRelatedField()
    spu_id = serializers.IntegerField()

    class Meta:
        model = SPUSpecification
        fields = ('id', 'name', 'spu', 'spu_id')


class SPUSpecificationSimpleSerializer(serializers.ModelSerializer):
    """

        规格管理SPUSpecification简单展示序列化器(simple)
    """

    name = serializers.SerializerMethodField()

    class Meta:
        model = SPUSpecification
        fields = ('id', 'name')

    def get_name(self, obj):
        return str(obj)


# ------------------------------------------ #


class SpecificationOptionSerializer(serializers.ModelSerializer):
    """

        SKU管理SpecificationOption规格选项序列化器
    """

    class Meta:
        model = SpecificationOption
        fields = ('id', 'value')


class PKSPUSpecificationSerializer(serializers.ModelSerializer):
    """SKU管理SPUSpecification序列化器"""
    # 关联查询
    spu = serializers.StringRelatedField()
    spu_id = serializers.IntegerField()
    options = SpecificationOptionSerializer(read_only=True, many=True)

    class Meta:
        model = SPUSpecification
        fields = ('id', 'name', 'spu', 'spu_id', 'options')


class SPUSerializer(serializers.ModelSerializer):
    """SPU信息"""
    brand = serializers.StringRelatedField()
    brand_id = serializers.IntegerField()
    category1_id = serializers.IntegerField()
    category2_id = serializers.IntegerField()
    category3_id = serializers.IntegerField()

    class Meta:
        model = SPU
        fields = (
            'id', 'name', 'brand', 'brand_id', 'category1_id',
            'category2_id', 'category3_id', 'sales', 'comments',
            'desc_detail', 'desc_pack', 'desc_service')


class BrandsSimpleSerializer(serializers.ModelSerializer):
    """添加spu信息简单展示Brands"""

    class Meta:
        model = Brand
        fields = '__all__'


class CategoriesSerializer(serializers.ModelSerializer):
    """
        添加spu展示商品分类
    """

    class Meta:
        model = GoodsCategory
        fields = ('id', 'name')


class ChannelGroupSerializer(serializers.ModelSerializer):
    """

        展示频道组
    """

    class Meta:
        model = GoodsChannelGroup
        fields = ('id', 'name')


class BrandSerializer(serializers.ModelSerializer):
    """

        品牌展示
    """

    def create(self, validated_data):
        image = validated_data['logo']
        # 上传到fdfs
        fdfs = Fdfs_client(settings.FDFS_CONF_DIR)
        ret = fdfs.upload_by_buffer(image.read())
        if ret['Status'] == 'Upload successed.':
            image_url = ret['Remote file_id']
            new_rand = Brand.objects.create(logo=image_url, name=validated_data.get('name'),
                                            first_letter=validated_data.get('first_letter'))
        else:
            raise ValueError('上传失败')

        return new_rand

    def update(self, instance, validated_data):
        pass

    class Meta:
        model = Brand
        fields = '__all__'
