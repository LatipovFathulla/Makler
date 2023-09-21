from modeltranslation.translator import register, TranslationOptions

from products.models import HouseModel, CategoryModel, AmenitiesModel, HowSaleModel, ComplaintModel


@register(CategoryModel)
class CategoryTranslationOptions(TranslationOptions):
    fields = ['title', 'subtitle']


@register(AmenitiesModel)
class AmenitiesModelTranslationOptions(TranslationOptions):
    fields = ['title']


@register(HowSaleModel)
class HowSaleModelTranslationOptions(TranslationOptions):
    fields = ['title']

# ComplaintModel
@register(ComplaintModel)
class ComplaintModelTranslationOptions(TranslationOptions):
    fields = ['reasons']


@register(HouseModel)
class HouseTranslationOptions(TranslationOptions):
    fields = ['title', 'descriptions']
