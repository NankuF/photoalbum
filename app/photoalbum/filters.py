import django_filters
from django_filters import DateTimeFilter, NumberFilter, CharFilter

from photoalbum.models import Album, Photo


class CustomAlbumFilter(django_filters.FilterSet):
    created = DateTimeFilter(field_name='created', lookup_expr='exact')
    created_gte = DateTimeFilter(field_name='created', lookup_expr='gte')
    created_lte = DateTimeFilter(field_name='created', lookup_expr='lte')
    created_gt = DateTimeFilter(field_name='created', lookup_expr='gt')
    created_lt = DateTimeFilter(field_name='created', lookup_expr='lt')

    images_count = NumberFilter(field_name='images_count', lookup_expr='exact')
    images_count_gte = NumberFilter(field_name='images_count', lookup_expr='gte')
    images_count_lte = NumberFilter(field_name='images_count', lookup_expr='lte')
    images_count_gt = NumberFilter(field_name='images_count', lookup_expr='gt')
    images_count_lt = NumberFilter(field_name='images_count', lookup_expr='lt')

    class Meta:
        model = Album
        fields = ('created', 'images_count')


class CustomPhotoFilter(django_filters.FilterSet):
    album_title = CharFilter(field_name='album__title', lookup_expr='icontains', label='Название альбома содержит')
    tag = CharFilter(field_name='tag', lookup_expr='icontains')

    class Meta:
        model = Photo
        fields = ('album', 'tag')
        # убираем автосоздание поля во всплывающем окне filter, не влияет на поля выше Meta
        exclude = ('album', 'tag')
