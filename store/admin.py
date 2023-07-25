from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from store.models import StoreModel, StoreAmenities, UseForModel, HowStoreServiceModel, StoreBrandModel


@admin.register(StoreAmenities)
class StoreAmenities(admin.ModelAdmin):
    list_display = ['title', 'created_at']


@admin.register(UseForModel)
class UseForModelAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at']


@admin.register(HowStoreServiceModel)
class HowStoreServiceModelAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at']


@admin.register(StoreBrandModel)
class StoreBrandModelAdmin(admin.ModelAdmin):
    list_display = ['title', 'br_image_tag', 'created_at']

    def br_image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" height="60" />'.format(obj.image.url))
        else:
            return '-'

    br_image_tag.short_description = _('Image')

@admin.register(StoreModel)
class StoreModelAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name', 'med_image_tag', 'med_brand_image_tag', 'price', 'phoneNumber', 'product_status', 'created_at']
    search_fields = ['pk', 'name', 'phoneNumber']
    list_filter = ['name', 'created_at']
    save_on_top = True
    save_as = True

    def med_image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" height="60" />'.format(obj.image.url))
        else:
            return '-'

    def med_brand_image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" height="60" />'.format(obj.brand_image.url))
        else:
            return '-'

    med_image_tag.short_description = _('Изображения')
    med_brand_image_tag.short_description = _('Изображения бренда')