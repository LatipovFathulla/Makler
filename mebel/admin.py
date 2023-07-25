from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

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
    list_display = ['pk', 'creator', 'title', 'mebel_image_tag', 'price', 'phone_number',
                    'web_address_title', 'product_status', 'created_at'
                    ]
    search_fields = ['title', 'creator', 'price']
    list_filter = ['created_at', 'price']
    inlines = [NewMebelImagesAdmin]

    def mebel_image_tag(self, obj):
        first_image = obj.images.first()  # Получаем первое изображение продукта из связанной модели
        if first_image:
            return format_html('<img src="{}" height="60" />'.format(first_image.images.url))
        else:
            return '-'

    mebel_image_tag.short_description = _('Image')
