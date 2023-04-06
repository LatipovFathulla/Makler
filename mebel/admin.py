from django.contrib import admin

from mebel.models import MebelCategoryModel, MebelModel, NewMebelImages


@admin.register(MebelCategoryModel)
class CategoryModelAdmin(admin.ModelAdmin):
    list_display = ['pk', 'created_at']
    search_fields = ['title']


class NewMebelImagesAdmin(admin.TabularInline):
    model = NewMebelImages
    extra = 1


@admin.register(MebelModel)
class MebelModelAdmin(admin.ModelAdmin):
    list_display = ['pk', 'created_at']
    search_fields = ['title']
    inlines = [NewMebelImagesAdmin]
