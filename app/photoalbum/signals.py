import os

from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from photoalbum.models import Photo


@receiver(post_delete, sender=Photo)
def post_delete_image(sender, instance, *args, **kwargs):
    """ Clean old image file """
    try:
        instance.image.delete(save=False)
        instance.thumbnail.delete(save=False)
    except:
        pass


@receiver(post_save, sender=Photo)
def create_thumbnail(sender, instance, *args, **kwargs):
    """Add thumbnail"""
    try:
        image_path = instance.image.path
        filename, extension = instance.image.name.split(os.sep)[1].split('.')
        thumbnail = Photo.create_thumbnail(image_path, filename, extension)
        instance.thumbnail = thumbnail
        instance.save()
    except:
        pass
