from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *


# TODO  а еще можно так
#  from django.contrib import admin
#  @admin.register(Shelter)
#  class ShelterAdmin(admin.ModelAdmin):
#      ...
#  без admin.site.register(Shelter, ShelterAdmin)

class ShelterAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', )
    list_display_links = ('pk', 'name')
    search_fields = ('name',)


class KindAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', )
    list_display_links = ('pk', 'name')
    search_fields = ('name',)


class PetAdmin(admin.ModelAdmin):
    # TODO выглядит неопрятно, используй  black
    list_display = ('pk', 'name', 'birthday', 'arrival_date', 'weight', 'height', 'deleted_at', 'shelter', 'kind')
    list_display_links = ('pk', 'name')
    search_fields = ('name', 'arrival_date', 'signs')
    list_editable = ('deleted_at',)
    list_filter = ('shelter', 'deleted_at', 'kind')
    fields = ('name', 'birthday', 'arrival_date',
              'signs', 'weight', 'height', 'photo',
              'get_photo', 'deleted_at', 'shelter', 'kind')
    readonly_fields = ('get_photo', 'arrival_date', 'birthday', 'shelter', 'kind')

    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="100">')

    get_photo.short_description = 'Миниатюра'

    def get_queryset(self, request):
        # TODO category?
        return Pet.objects.all().select_related('category')


admin.site.register(Shelter, ShelterAdmin)
admin.site.register(Kind, KindAdmin)
admin.site.register(Pet, PetAdmin)
