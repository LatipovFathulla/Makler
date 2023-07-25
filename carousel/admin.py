from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from carousel.models import CarouselModel, BannerADSModel


@admin.register(CarouselModel)
class CarouselModelAdmin(admin.ModelAdmin):
    list_display = ['pk', 'carousel_image_tag', 'created_at']
    search_fields = ['pk']

    def carousel_image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" height="60" />'.format(obj.image.url))
        else:
            return '-'

    carousel_image_tag.short_description = _('Image')


@admin.register(BannerADSModel)
class BannerADSModel(admin.ModelAdmin):
    list_display = ['pk', 'banner_image_tag', 'url', 'created_at']
    search_fields = ['pk']

    def banner_image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" height="60" />'.format(obj.image.url))
        else:
            return '-'

    banner_image_tag.short_description = _('Image')