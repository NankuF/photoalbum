from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models


class Album(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Владелец', blank=True)
    title = models.CharField(max_length=255, blank=False, verbose_name='Название альбома', unique=True)
    images_count = models.PositiveIntegerField(verbose_name='Количество фото в альбоме', default=0)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        ordering = ('-created',)
        verbose_name = 'альбом'
        verbose_name_plural = 'альбомы'

    def __str__(self):
        return self.title


def image_size(value):
    limit = settings.IMAGE_SIZE_LIMIT * 1024 * 1024
    if value.size > limit:
        raise ValidationError('Размер изображения не должен превышать 5 mb.')


class Photo(models.Model):
    """
    Валидация по размеру файла и расширению.
    """
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='photo_album', verbose_name='Альбом')
    title = models.CharField(max_length=255, verbose_name='Название фотографии', unique=True)
    image = models.ImageField(upload_to='images',
                              max_length=250,
                              verbose_name='Изображение',
                              validators=[
                                  image_size,
                                  FileExtensionValidator(
                                      settings.IMAGE_EXTENSIONS,
                                      message=f'Разрешённые расширения: {", ".join(settings.IMAGE_EXTENSIONS)}'
                                  ),
                              ])
    thumbnail = models.ImageField(upload_to='thumbnails', verbose_name='Миниатюра', blank=True)
    tag = models.CharField(max_length=30, verbose_name='Тэг', blank=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        ordering = ('-created',)
        verbose_name = 'фотография'
        verbose_name_plural = 'фотографии'

    def __str__(self):
        return self.title
