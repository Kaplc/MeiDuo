# Generated by Django 3.2.16 on 2022-11-27 08:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('oauth', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='oauthqquser',
            old_name='creat_time',
            new_name='create_time',
        ),
    ]
