# Generated by Django 3.0.5 on 2023-03-10 21:40

import common.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(default='', max_length=50, verbose_name='用户名')),
                ('password', models.CharField(default='', max_length=128, verbose_name='密码')),
                ('name', models.CharField(default='', max_length=50, verbose_name='姓名')),
                ('sex', models.CharField(choices=[('男', '男'), ('女', '女')], default='', max_length=512, verbose_name='性别')),
                ('mobile', models.CharField(default='', max_length=50, verbose_name='手机')),
                ('email', models.CharField(default='', max_length=50, verbose_name='邮箱')),
                ('idcard', models.CharField(default='', max_length=50, verbose_name='身份证')),
                ('photo', common.models.MyImageField(default='', max_length=255, verbose_name='头像')),
            ],
            options={
                'verbose_name': '用户',
                'verbose_name_plural': '用户',
                'db_table': 'users',
            },
        ),
    ]
