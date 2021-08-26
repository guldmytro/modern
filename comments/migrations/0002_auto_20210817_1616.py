# Generated by Django 3.2.6 on 2021-08-17 13:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_alter_post_excerpt'),
        ('comments', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_comments', to='blog.post', verbose_name='Запись с Блога'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='reply',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replied_comments', to='comments.comment', verbose_name='Ответ на комментарий'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='status',
            field=models.CharField(choices=[('draft', 'Ждет модерации'), ('published', 'Опубликовано')], default='published', max_length=15, verbose_name='Статус'),
        ),
    ]