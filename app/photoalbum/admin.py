from django.contrib import admin
from django.db.models import F

from photoalbum.models import Photo, Album


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ('username', 'title', 'images_count', 'created')
    list_filter = ('created', 'images_count')
    readonly_fields = ('created', 'images_count', 'username')
    list_display_links = ('title',)

    # Делаем красивое разделение детальной информации внутри альбома.
    fieldsets = (
        ('Название альбома', {
            'fields': ('username', 'title')
        }),
        ('Характеристики', {
            'fields': ('images_count', 'created')
        }),
    )

    def get_queryset(self, request):
        """Залогиненый юзер видит только свои записи в админке"""
        qs = super(AlbumAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(username=request.user)

    def save_model(self, request, obj, form, change):
        """Владельцем альбома автоматически станет создавший его юзер"""
        if getattr(obj, 'username', None) is None:
            obj.username = request.user
        obj.save()


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('title', 'image', 'thumbnail', 'album', 'tag', 'created', )
    list_filter = ('created', 'album')
    readonly_fields = ('created', 'thumbnail')
    exclude = ('thumbnail',)

    def render_change_form(self, request, context, *args, **kwargs):
        """ Показывать список альбомов, принадлежащий только этому юзеру, при нажатии "Добавить" """
        context['adminform'].form.fields['album'].queryset = Album.objects.filter(username=request.user)
        return super(PhotoAdmin, self).render_change_form(request, context, *args, **kwargs)

    def get_queryset(self, request):
        """Юзер видит только принадлежащие ему фотографии"""
        qs = super(PhotoAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(album__username=request.user)

    def delete_queryset(self, request, queryset):
        """При удалении фотографии уменьшается счетчик фото в альбоме"""
        for photo in queryset:
            if photo.album_id and photo.album.images_count > 0:
                Album.objects.filter(pk=photo.album_id).update(images_count=F('images_count') - 1)
            super(PhotoAdmin, self).delete_queryset(request, queryset)
