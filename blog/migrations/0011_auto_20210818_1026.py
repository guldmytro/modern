# Generated by Django 3.2.6 on 2021-08-18 07:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_auto_20210818_1009'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='category',
        ),
        migrations.AddField(
            model_name='post',
            name='category',
            field=models.ManyToManyField(null=True, to='blog.Tag', verbose_name='Категория'),
        ),
    ]
