from django.db import models
from django.conf import settings
from django.utils import timezone
from django.urls import reverse
from django.core.validators import FileExtensionValidator


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='published')


class Tag(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    thumbnail = models.FileField(upload_to='images/%Y/%m/%d',
                                 validators=[FileExtensionValidator(['png', 'jpg', 'svg'])],
                                 verbose_name='Изображение',
                                 help_text='Поддерживаются форматы: .png, .jpg, .svg',
                                 blank=True,
                                 null=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:blog_by_tag', args=[self.slug])


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Черновик'),
        ('published', 'Опубликовано'),
    )
    title = models.CharField(verbose_name='Заголовок', max_length=250)
    slug = models.SlugField(verbose_name='Слаг', max_length=250, unique_for_date='publish')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='blog_posts',
                               editable=False, blank=True, null=True, verbose_name='Автор')
    category = models.ForeignKey(Tag, verbose_name='Категория', on_delete=models.SET_NULL, null=True)
    thumbnail = models.ImageField(upload_to='images/%Y/%m/%d')
    content = models.TextField(verbose_name="Контент", blank=True)
    excerpt = models.TextField(verbose_name='Краткое описание', max_length=500)

    status = models.CharField(verbose_name="Статус", max_length=15, choices=STATUS_CHOICES, default='draft')
    publish = models.DateTimeField(verbose_name="Опубликовано", default=timezone.now)
    created = models.DateTimeField(verbose_name="Создано", auto_now_add=True)
    updated = models.DateTimeField(verbose_name="Оновлено", auto_now=True)

    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        ordering = ('-publish',)
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.publish.year, self.publish.month, self.publish.day, self.slug])

