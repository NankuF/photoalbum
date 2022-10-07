from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter

from .filters import CustomAlbumFilter, CustomPhotoFilter
from .models import Album, Photo
from .serializers import AlbumSerializer, PhotoSerializer


class AlbumViewSet(viewsets.ModelViewSet):
    serializer_class = AlbumSerializer
    # для фильтра бекенда ставится django-filter
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    # кастомные классы вместо filterset_fields
    filterset_class = CustomAlbumFilter
    search_fields = ('title',)
    ordering_fields = ('created', 'images_count')

    def get_queryset(self):
        """Показать альбомы пользователя"""
        return Album.objects.filter(username=self.request.user)

    def perform_create(self, serializer):
        """При создании альбома владельцем становится тот, кто его создал."""
        if self.request.user.is_authenticated:
            instance = serializer.save(username=self.request.user)


class PhotoViewSet(viewsets.ModelViewSet):
    serializer_class = PhotoSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_class = CustomPhotoFilter
    search_fields = ('tag',)
    ordering_fields = ('created', 'album__title')

    def get_queryset(self):
        return Photo.objects.filter(album__username=self.request.user)
