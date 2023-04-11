from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from products.models import CategoryModel, HouseModel, AmenitiesModel, \
    HouseImageModel, PriceListModel, HowSaleModel, NewHouseImages


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
    list_display = ['title', 'created_at']
    search_fields = ['title', 'created_at']
    list_filter = ['created_at']
    save_as = True


@admin.register(HowSaleModel)
class HowSaleModelAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_at']
    search_fields = ['title', 'created_at']
    save_as = True


@admin.register(AmenitiesModel)
class AmenitiesModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'created_at']
    search_fields = ['title', 'created_at']
    list_filter = ['created_at']
    save_as = True


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

class NewHouseImagesInline(admin.TabularInline):
    model = NewHouseImages
    extra = 1


@admin.register(HouseModel)
class HouseModelAdmin(MyTranslationAdmin):
    list_display = ['pk', 'title', 'price', 'category', 'type', 'product_status', 'created_at']
    search_fields = ['title', 'type']
    list_filter = ['created_at']
    inlines = [NewHouseImagesInline]
    save_as = True
    save_on_top = True
