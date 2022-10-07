from rest_framework import serializers

from .models import Album, Photo


class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = '__all__'
        read_only_fields = ('images_count', 'created', 'username')


#
class UserAlbumForeignKey(serializers.PrimaryKeyRelatedField):
    """Показывать альбомы принадлежащие юзеру"""

    def get_queryset(self):
        user = self.context['request'].user
        return Album.objects.filter(username=user)


class PhotoSerializer(serializers.ModelSerializer):
    album = UserAlbumForeignKey()

    class Meta:
        model = Photo
        fields = '__all__'
        read_only_fields = ('created', 'thumbnail')

    def get_user(self, obj):
        return str(obj.user.username)
