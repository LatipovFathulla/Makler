from django.contrib import admin
from modeltranslation.admin import TranslationAdmin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from products.models import CategoryModel, HouseModel, AmenitiesModel, \
    HouseImageModel, PriceListModel, HowSaleModel, NewHouseImages, Complaint, ComplaintModel


class MyTranslationAdmin(TranslationAdmin):
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }



@admin.register(CategoryModel)
class CategoryModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'cat_image_tag', 'created_at']
    search_fields = ['id', 'title', 'created_at']
    list_filter = ['created_at']
    save_as = True

    def cat_image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" height="60" />'.format(obj.image.url))
        else:
            return '-'

    cat_image_tag.short_description = _('Image')

@admin.register(HowSaleModel)
class HowSaleModelAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at']
    search_fields = ['title', 'created_at']
    save_as = True


@admin.register(AmenitiesModel)
class AmenitiesModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'amenities_image_tag', 'created_at']
    search_fields = ['title', 'created_at']
    list_filter = ['created_at']
    save_as = True

    def amenities_image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" height="60" />'.format(obj.image.url))
        else:
            return '-'

    amenities_image_tag.short_description = _('Image')

@admin.register(PriceListModel)
class PriceListModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'price_t', 'created_at']
    save_as = True



# @admin.register(HouseImageModel)
# class HouseImageModelAdmin(admin.ModelAdmin):
#     list_display = ['pk', 'image', 'created_at']
#     search_fields = ['created_at']
#     list_filter = ['created_at']

# @admin.register(NewHouseImages)
# class NewHouseImagesAdmin(admin.ModelAdmin):
#     list_display = ['pk', 'product', 'images']
@admin.register(ComplaintModel)
class ComplaintModelAdmin(admin.ModelAdmin):
    list_display = ['pk', 'reasons']

@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ['user', 'reason', 'created_at']
    list_filter = ['reason']
    search_fields = ['user__username', 'reason', 'created_at']

class NewHouseImagesInline(admin.TabularInline):
    model = NewHouseImages
    extra = 1


@admin.register(HouseModel)
class HouseModelAdmin(MyTranslationAdmin):
    list_display = ['pk', 'title', 'price', 'house_image_tag', 'category', 'type', 'product_status', 'created_at']
    search_fields = ['title', 'type']
    list_filter = ['created_at']
    inlines = [NewHouseImagesInline]
    save_as = True
    save_on_top = True

    def house_image_tag(self, obj):
        first_image = obj.images.first()  # Получаем первое изображение продукта из связанной модели
        if first_image:
            return format_html('<img src="{}" height="60" />'.format(first_image.images.url))
        else:
            return '-'

    house_image_tag.short_description = _('Image')
