from os import walk

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import transaction
from django.test import TestCase
from mixer.backend.django import mixer
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate

from photoalbum.models import Album
from .models import Photo
from .views import AlbumViewSet


class TestAlbumModel(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='test1', email='test1@test.com', password='Z123xcvbnm'
        )
        self.album = Album.objects.create(
            username=self.user,
            title='my_album',
            images_count=0,
        )
        return super().setUp()

    def test_create_album(self):
        self.assertEqual(self.album.username, self.user)
        self.assertEqual(self.album.title, 'my_album')
        self.assertEqual(self.album.images_count, 0)


class TestPhotoModel(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='test1', email='test1@test.com', password='Z123xcvbnm'
        )
        with transaction.atomic():
            self.album = Album.objects.create(
                username=self.user,
                title='my_album',
                images_count=0,
            )

            self.photo = Photo.objects.create(
                album=self.album,
                title='фото',
                image=SimpleUploadedFile(name='test_image.jpg',
                                         content=open('photoalbum/test_dir/top.jpg', 'rb').read(),
                                         content_type='image/jpeg'),
            )
        super().setUp()

    def test_create_photo(self):
        self.assertIn('.jpg', self.photo.image.name)
        self.photo.delete()

    def test_create_thumbnail(self):
        self.assertIn('resized.jpg', self.photo.thumbnail.name)
        self.photo.delete()

    def test_delete_photo(self):
        self.photo.delete()
        mypath = 'media/images'
        photos = []
        for (dirpath, dirnames, filenames) in walk(mypath):
            photos.extend(filenames)
            break
        self.assertEqual(len(photos), 0)


class TestAPIAlbum(TestCase):

    def setUp(self):
        self.super_user = get_user_model().objects.create_superuser(
            username='admintest', email='admin@test.com', password='Z123xcvbnm'
        )
        self.user = get_user_model().objects.create_user(
            username='test1', email='test1@test.com', password='Z123xcvbnm')

        self.factory = APIRequestFactory()
        self.album = mixer.blend(Album, username=self.user)

    def test_get_list_quest(self):
        view = AlbumViewSet.as_view({'get': 'list'})
        request = self.factory.get('api/v1/albums/')
        response = view(request)
        # print(response.render().content.decode('utf-8'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_list_user(self):
        view = AlbumViewSet.as_view({'get': 'list'})
        request = self.factory.get('api/v1/albums/')
        force_authenticate(request, user=self.user)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_detail_quest(self):
        view = AlbumViewSet.as_view({'get': 'retrieve'})
        request = self.factory.get(f'api/v1/albums/{self.album.id}')
        response = view(request, pk=self.album.pk)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_detail_user(self):
        view = AlbumViewSet.as_view({'get': 'retrieve'})
        request = self.factory.get(f'api/v1/albums/{self.album.id}')
        force_authenticate(request, self.user)
        response = view(request, pk=self.album.pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_quest(self):
        view = AlbumViewSet.as_view({'post': 'create'})
        album_data = {'title': 'new_album'}
        request = self.factory.post('api/v1/albums/', self.album.title, format='json')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_post_user(self):
        view = AlbumViewSet.as_view({'post': 'create'})
        album = {'title': 'new_album'}
        request = self.factory.post('api/v1/albums/', album, format='json')
        force_authenticate(request, user=self.user)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete_quest(self):
        view = AlbumViewSet.as_view({'delete': 'destroy'})
        request = self.factory.delete(f'api/v1/albums/{self.album.pk}')
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_user(self):
        view = AlbumViewSet.as_view({'delete': 'destroy'})
        request = self.factory.delete(f'api/v1/albums/{self.album.pk}')
        force_authenticate(request, self.user)
        response = view(request, pk=self.album.pk)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Album.objects.filter(pk=self.album.id).exists())
