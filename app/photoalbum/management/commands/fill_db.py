import os
import random

from PIL import Image
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.core.management import BaseCommand
from mixer.backend.django import mixer

from photoalbum.models import Album, Photo


def create_image():
    x = random.randrange(0, 1000)
    width = 700
    height = 300

    img = Image.new(mode="RGB", size=(width, height))
    path = os.path.join(settings.MEDIA_ROOT, settings.IMAGES_DIR, f'photo_{x}.jpg')
    img.save(path)
    fullpath, basename = os.path.split(path)
    last_dir = f'{os.sep}'.join(fullpath.split(os.sep)[-1:])
    return os.path.join(last_dir, basename)


class Command(BaseCommand):
    help = "Fill the database with data"

    def handle(self, *args, **kwargs):
        User.objects.all().delete()
        Album.objects.all().delete()
        Photo.objects.all().delete()

        user = get_user_model().objects.create_superuser(username='admin', password='123')
        admin_album = mixer.blend(Album, username=user)
        for _ in range(4):
            Photo.objects.create(
                album=admin_album,
                title=f'hello_{random.randrange(0, 1000)}',
                image=create_image()
            )

        users = mixer.cycle(2).blend(User)
        albums = mixer.cycle(3).blend(Album, username=mixer.sequence(*users))
        for album in albums:
            for _ in range(3):
                Photo.objects.create(
                    album=album,
                    title=f'hello_{random.randrange(0, 1000)}',
                    image=create_image()
                )
