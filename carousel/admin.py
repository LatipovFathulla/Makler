from django.contrib import admin

from carousel.models import CarouselModel


@admin.register(CarouselModel)
class CarouselModelAdmin(admin.ModelAdmin):
    list_display = ['pk', 'image', 'created_at']
    search_fields = ['pk']
