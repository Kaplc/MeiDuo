# Generated by Django 3.2.18 on 2023-04-07 22:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0010_spudetailimage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='spudetailimage',
            name='spu',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='detail_image', to='goods.spu', verbose_name='商品SPU'),
        ),
    ]