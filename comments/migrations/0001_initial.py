# Generated by Django 3.2.6 on 2021-08-16 14:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Имя')),
                ('surname', models.CharField(max_length=50, verbose_name='Фамилия')),
                ('comment', models.TextField(verbose_name='Комментарий')),
                ('publish', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('draft', 'Ждет модерации'), ('published', 'Опубликовано')], default='published', max_length=15)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_comments', to='blog.post')),
                ('reply', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='replied_comments', to='comments.comment', verbose_name='Ответ на комментарий')),
            ],
            options={
                'ordering': ('-publish',),
            },
        ),
    ]
