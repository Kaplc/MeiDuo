# Generated by Django 4.1.3 on 2022-11-21 16:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_email_active_area'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Area',
        ),
    ]
