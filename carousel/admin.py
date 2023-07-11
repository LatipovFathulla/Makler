from django.contrib import admin

from carousel.models import CarouselModel, BannerADSModel


@admin.register(CarouselModel)
class CarouselModelAdmin(admin.ModelAdmin):
    list_display = ['pk', 'image', 'created_at']
    search_fields = ['pk']


@admin.register(BannerADSModel)
class BannerADSModel(admin.ModelAdmin):
    list_display = ['pk', 'image', 'created_at']
    search_fields = ['pk']
