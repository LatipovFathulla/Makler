from django.contrib import admin

from mebel.models import MebelCategoryModel, MebelModel


@admin.register(MebelCategoryModel)
class CategoryModelAdmin(admin.ModelAdmin):
    list_display = ['pk', 'created_at']
    search_fields = ['title']


@admin.register(MebelModel)
class MebelModelAdmin(admin.ModelAdmin):
    list_display = ['pk', 'created_at']
    search_fields = ['title']
