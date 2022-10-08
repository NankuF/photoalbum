import os

from PIL import Image
from PIL.Image import Resampling
from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models
from django.db.models import F


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
    image = models.ImageField(upload_to=settings.IMAGES_DIR,
                              max_length=250,
                              verbose_name='Изображение',
                              validators=[
                                  image_size,
                                  FileExtensionValidator(
                                      settings.IMAGE_EXTENSIONS,
                                      message=f'Разрешённые расширения: {", ".join(settings.IMAGE_EXTENSIONS)}'
                                  ),
                              ])
    thumbnail = models.ImageField(upload_to='images/thumbnails', verbose_name='Миниатюра', blank=True)
    tag = models.CharField(max_length=30, verbose_name='Тэг', blank=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        ordering = ('-created',)
        verbose_name = 'фотография'
        verbose_name_plural = 'фотографии'

    def __str__(self):
        return self.title

    @staticmethod
    def create_thumbnail(image_path, filename, extension):
        thumbnail_path = os.path.join(settings.MEDIA_ROOT, settings.IMAGES_DIR, 'thumbnails')
        if not os.path.exists(thumbnail_path):
            os.makedirs(thumbnail_path, exist_ok=True)
        resized_file_fullpath = os.path.join(thumbnail_path, f'{filename}_resized.{extension}')
        resized_file = open(resized_file_fullpath, "w")
        MAX_SIZE = 150
        image = Image.open(image_path)

        if image.size[0] > image.size[1]:
            resized_width = MAX_SIZE
            resized_height = int(round((MAX_SIZE / float(image.size[0])) * image.size[1]))
        else:
            resized_height = MAX_SIZE
            resized_width = int(round((MAX_SIZE / float(image.size[1])) * image.size[0]))

        image = image.resize((resized_width, resized_height), Resampling.LANCZOS)
        image.save(resized_file, 'JPEG')
        fullpath, basename = os.path.split(resized_file.name)
        last_two_dirs = f'{os.sep}'.join(fullpath.split(os.sep)[-2:])
        return os.path.join(last_two_dirs, basename)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.pk:
            Album.objects.filter(pk=self.album_id).update(images_count=F('images_count') + 1)
        super(Photo, self).save()
        filename_with_extension = self.image.name.split('/')[-1]
        filename, extension = filename_with_extension.split('.')
        images_path = os.path.join(settings.MEDIA_ROOT, settings.IMAGES_DIR, filename_with_extension)
        thumbnail = self.create_thumbnail(images_path,filename, extension)
        self.thumbnail = thumbnail
        super(Photo, self).save()

    def delete(self, using=None, keep_parents=False):
        """Удалит фото и миниатюру с диска и уменьшит счетчик фото в альбоме"""
        if self.album_id and self.album.images_count > 0:
            Album.objects.filter(pk=self.album_id).update(images_count=F('images_count') - 1)
        if os.path.exists(self.image.path):
            os.remove(self.image.path)
        if os.path.exists(self.thumbnail.path):
            os.remove(self.thumbnail.path)
        super(Photo, self).delete()
