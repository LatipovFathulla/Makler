from modeltranslation.translator import register, TranslationOptions

from products.models import HouseModel, CategoryModel, AmenitiesModel, HowSaleModel


@register(CategoryModel)
class CategoryTranslationOptions(TranslationOptions):
    fields = ['title', 'subtitle']


@register(AmenitiesModel)
class AmenitiesModelTranslationOptions(TranslationOptions):
    fields = ['title']


@register(HowSaleModel)
class HowSaleModelTranslationOptions(TranslationOptions):
    fields = ['title']


@register(HouseModel)
class HouseTranslationOptions(TranslationOptions):
    fields = ['title', 'descriptions']
