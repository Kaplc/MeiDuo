from fdfs_client.client import Fdfs_client
from rest_framework import serializers
from goods.models import SPUSpecification, SKUImage, SKU, GoodsCategory, SKUSpecification
from celery_tasks.generate_static.tasks import detail_page
from django.conf import settings


class SPUSpecificationSerializer(serializers.ModelSerializer):
    """规格管理SPUSpecification序列化器"""
    # 关联查询
    spu = serializers.StringRelatedField()
    spu_id = serializers.IntegerField()

    class Meta:
        model = SPUSpecification
        fields = ('id', 'name', 'spu', 'spu_id')


class SPUSpecificationSimpleSerializer(serializers.ModelSerializer):
    """规格管理SPUSpecification简单展示序列化器(simple)"""

    class Meta:
        model = SPUSpecification
        fields = ('id', 'name')


class ImageSerializer(serializers.ModelSerializer):
    """图片管理SKUImage序列化器"""

    class Meta:
        model = SKUImage
        fields = ('id', 'sku', 'image')

    def create(self, validated_data):
        """重写序列化器create"""
        image = validated_data['image']
        sku = validated_data['sku']
        # 上传到fdfs
        fdfs = Fdfs_client(settings.FDFS_CONF_DIR)
        ret = fdfs.upload_by_buffer(image.read())
        if ret['Status'] == 'Upload successed.':
            image_url = ret['Remote file_id']
            sku_image = SKUImage.objects.create(image=image_url, sku_id=sku.id)
            sku_image.save()
            # celery页面静态化
            detail_page.delay(sku.id)

        else:
            raise ValueError('上传失败')

        return sku_image

    def update(self, instance, validated_data):
        """重写更新"""
        image = validated_data['image']
        sku = validated_data['sku']
        # 上传到fdfs
        fdfs = Fdfs_client(settings.FDFS_CONF_DIR)
        # 修改上传的文件
        ret = fdfs.upload_by_buffer(image.read(), instance.image.name)
        if ret['Status'] == 'Upload successed.':
            image_url = ret['Remote file_id']
            update_sku_image, res = SKUImage.objects.update_or_create(id=instance.id, defaults={'image': image_url})
            # celery页面静态化
            detail_page.delay(sku.id)

        else:
            raise ValueError('上传失败')

        return update_sku_image


class ImageToSKUSimpleSerializer(serializers.ModelSerializer):
    """图片管理展示简单sku信息"""

    class Meta:
        model = SKU
        fields = ('id', 'name',)


class CategoriesSerializer(serializers.ModelSerializer):
    """Categories信息"""

    class Meta:
        model = GoodsCategory
        fields = ('id', 'name')

    """
    {
        "counts": "商品SPU总数量",
        "lists": [
            {
                "id": "商品SKU ID",
                "name": "商品SKU名称",
                "spu": "商品SPU名称",
                "spu_id": "商品SPU ID",
                "caption": "商品副标题",
                "category_id": "三级分类id",
                "category": "三级分类名称",
                "price": "价格",
                "cost_price": "进价",
                "market_price": "市场价格",
                "stock": "库存",
                "sales": "销量",
                "is_launched": "上下架",
                "specs": [
                    {
                        "spec_id": "规格id",
                        "option_id": "选项id"
                    },
                    ...
                ]
            },
            {
    """


class SKUSpecificationSerializer(serializers.ModelSerializer):
    """SKUSerializer嵌套查询SPUSpecification"""
    option_id = serializers.IntegerField()
    spec_id = serializers.IntegerField()

    class Meta:
        model = SKUSpecification
        fields = ('spec_id', 'option_id')


class SKUSerializer(serializers.ModelSerializer):
    """所有sku信息"""
    spu = serializers.StringRelatedField()
    category = serializers.StringRelatedField()
    specs = SKUSpecificationSerializer(read_only=True, many=True)

    class Meta:
        model = SKU
        fields = ('id', 'name', 'spu', 'spu_id',
                  'caption', 'category_id', 'category',
                  'price', 'cost_price', 'market_price', 'stock',
                  'sales', 'is_launched', 'specs')
