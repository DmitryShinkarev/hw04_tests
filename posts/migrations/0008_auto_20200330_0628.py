# Generated by Django 2.2 on 2020-03-30 06:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0007_auto_20200330_0622'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='group_posts',
            new_name='group',
        ),
    ]
