from typing import Union

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.db.models import QuerySet
from django.http import HttpRequest
from django.utils.safestring import mark_safe

from .models import *


@admin.register(Shelters)
class ShelterAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "name",
    )
    list_display_links = ("pk", "name")
    search_fields = ("name",)


@admin.register(Kinds)
class KindAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "name",
    )
    list_display_links = ("pk", "name")
    search_fields = ("name",)


@admin.register(Pets)
class PetAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "name",
        "birthday",
        "arrival_date",
        "weight",
        "height",
        "deleted",
        "shelter",
        "kind",
    )
    list_display_links = ("pk", "name")
    search_fields = ("name", "arrival_date", "signs")
    list_editable = ("deleted",)
    list_filter = ("shelter", "deleted", "kind")
    fields = (
        "name",
        "birthday",
        "arrival_date",
        "signs",
        "weight",
        "height",
        "photo",
        "get_photo",
        "deleted",
        "shelter",
        "kind",
    )
    readonly_fields = (
        "get_photo",
        "arrival_date",
    )

    def get_photo(self, obj: Pets) -> Union[str, None]:
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="100">')

    get_photo.short_description = "Миниатюра"

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        return Pets.all_objects.all().select_related("shelter")


@admin.register(ShelterUser)
class ShelterUserAdmin(UserAdmin):
    UserAdmin.fieldsets[0][1]['fields'] += ('shelter',)
    fieldsets = UserAdmin.fieldsets
