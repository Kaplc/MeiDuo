from django.db import transaction
from fdfs_client.client import Fdfs_client
from rest_framework import serializers
from celery_tasks.generate_static.tasks import detail_page
from django.conf import settings

from goods.models import SKUImage, SKU, SKUSpecification, GoodsCategory


class CategoriesSerializer(serializers.ModelSerializer):
    """Categories信息"""

    class Meta:
        model = GoodsCategory
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


class SKUSimpleSerializer(serializers.ModelSerializer):
    """图片管理展示简单sku信息"""

    class Meta:
        model = SKU
        fields = ('id', 'name',)


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
    specs = SKUSpecificationSerializer(many=True)

    # 返回模型类类的spu_id和category_id
    spu_id = serializers.IntegerField()
    category_id = serializers.IntegerField()

    def update(self, instance, validated_data):

        # 获取前端post数据
        specs = validated_data.get('specs')
        # sku保存时不用spec所以删除
        del validated_data['specs']

        with transaction.atomic():
            # 开启事务
            sid = transaction.savepoint()
            try:
                old_sku = SKU.objects.create(**validated_data)

                for spec in specs:
                    sku_specification = SKUSpecification.objects.create(sku=old_sku, spec_id=spec['spec_id'],
                                                                        option_id=spec['option_id'])
            except Exception as e:
                # 捕获异常，说明数据库操作失败，进行回滚
                transaction.savepoint_rollback(sid)
                return serializers.ValidationError('数据库错误')
            else:
                # 没有捕获异常，数据库操作成功，进行提交
                transaction.savepoint_commit(sid)
                # 执行异步任务生成新的静态页面
                detail_page.delay(old_sku.id)
                return old_sku

    def create(self, validated_data):
        # 获取前端post数据
        specs = validated_data.get('specs')
        # sku保存时不用spec所以删除
        del validated_data['specs']

        with transaction.atomic():
            # 开启事务
            sid = transaction.savepoint()
            try:
                new_sku = SKU.objects.create(**validated_data)

                for spec in specs:
                    sku_specification = SKUSpecification.objects.create(sku=new_sku, spec_id=spec['spec_id'],
                                                                        option_id=spec['option_id'])
            except Exception as e:
                # 捕获异常，说明数据库操作失败，进行回滚
                transaction.savepoint_rollback(sid)
                return serializers.ValidationError('数据库错误')
            else:
                # 没有捕获异常，数据库操作成功，进行提交
                transaction.savepoint_commit(sid)
                # 执行异步任务生成新的静态页面
                detail_page.delay(new_sku.id)
                return new_sku

    class Meta:
        model = SKU
        fields = ('id', 'name', 'spu', 'spu_id',
                  'caption', 'category_id', 'category',
                  'price', 'cost_price', 'market_price', 'stock',
                  'sales', 'is_launched', 'specs')
