from fdfs_client.client import Fdfs_client
from rest_framework import serializers
from goods.models import SPUSpecification, SKUImage, SKU, GoodsCategory
from celery_tasks.generate_static.tasks import detail_page
from django.conf import settings


class CategoriesSerializer(serializers.ModelSerializer):
    """Categories信息"""

    class Meta:
        model = GoodsCategory
        fields = ('id', 'name')


class SKUSerializer(serializers.ModelSerializer):
    """所有sku信息"""

    class Meta:
        model = SKU
        fields = '__all__'


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


class SKUSimpleSerializer(serializers.ModelSerializer):
    """简单sku信息    """

    class Meta:
        model = SKU
        fields = ('id', 'name',)
