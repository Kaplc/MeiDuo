# Generated by Django 3.2.18 on 2023-04-07 22:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0009_goodsvisitcount'),
    ]

    operations = [
        migrations.CreateModel(
            name='SPUDetailImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('image_url', models.ImageField(blank=True, default='', max_length=200, null=True, upload_to='', verbose_name='详情图片')),
                ('spu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.spu', verbose_name='spu')),
            ],
            options={
                'verbose_name': 'spu详情信息图片',
                'verbose_name_plural': 'spu详情信息图片',
                'db_table': 'tb_spu_detail_image',
            },
        ),
    ]