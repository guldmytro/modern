from django.db import models


class About(models.Model):

    name = models.CharField(max_length=100, verbose_name='Имя и Фамилия автора')
    excerpt = models.TextField(max_length=300, verbose_name='Краткое описание преимуществ / интересов автора')
    thumbnail = models.ImageField(verbose_name='Фото', upload_to='images/%Y/%m/%d')
    content = models.TextField(verbose_name="Контент")
    email = models.EmailField()

    class Meta:
        verbose_name = 'Страница об авторе'
        verbose_name_plural = 'Страница об авторе'

    def __str__(self):
        return self.name
