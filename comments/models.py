from django.db import models
from blog.models import Post


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='published')


class Comment(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Ждет модерации'),
        ('published', 'Опубликовано'),
    )
    name = models.CharField(verbose_name='Имя', max_length=50)
    surname = models.CharField(verbose_name='Фамилия', max_length=50)
    comment = models.TextField(verbose_name='Комментарий')
    reply = models.ForeignKey('self', verbose_name='Ответ на комментарий', blank=True, on_delete=models.CASCADE,
                              related_name='replied_comments',
                              null=True)
    post = models.ForeignKey(Post, verbose_name='Запись с Блога', related_name='post_comments',
                             on_delete=models.CASCADE)
    publish = models.DateTimeField(auto_now_add=True)
    status = models.CharField(verbose_name='Статус', max_length=15, choices=STATUS_CHOICES, default='published')

    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        ordering = ('-publish',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.comment

    def full_name(self):
        return f'{self.name} {self.surname}'
