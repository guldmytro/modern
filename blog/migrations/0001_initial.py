# Generated by Django 3.2.6 on 2021-08-16 14:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('slug', models.SlugField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250, verbose_name='Заголовок')),
                ('slug', models.SlugField(max_length=250, unique_for_date='publish', verbose_name='Слаг')),
                ('thumbnail', models.ImageField(upload_to='images/%Y/%m/%d')),
                ('content', models.TextField(blank=True)),
                ('status', models.CharField(choices=[('draft', 'Черновик'), ('published', 'Опубликовано')], default='draft', max_length=15)),
                ('publish', models.DateTimeField(default=django.utils.timezone.now)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.PROTECT, related_name='blog_posts', to=settings.AUTH_USER_MODEL)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='blog.tag', verbose_name='Категория')),
            ],
            options={
                'ordering': ('-publish',),
            },
        ),
    ]
