# Generated by Django 3.2.16 on 2022-11-28 13:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0003_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sku',
            old_name='default_image_url',
            new_name='default_image',
        ),
    ]
