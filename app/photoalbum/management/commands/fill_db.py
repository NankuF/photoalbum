from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.core.management import BaseCommand
from mixer.backend.django import mixer

from photoalbum.models import Album, Photo


class Command(BaseCommand):
    help = "Fill the database with data"

    def handle(self, *args, **kwargs):
        User.objects.all().delete()
        Album.objects.all().delete()
        Photo.objects.all().delete()

        user = get_user_model().objects.create_superuser(username='admin', password='123')
        admin_album = mixer.blend(Album, username=user)
        mixer.cycle(2).blend(Photo, album__username=user, album=admin_album)

        users = mixer.cycle(2).blend(User)
        for user in users:
            album = mixer.cycle(3).blend(Album, username=user)
            mixer.cycle(3).blend(Photo, album=mixer.sequence(*album))
