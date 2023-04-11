from modeltranslation.translator import register, TranslationOptions

from products.models import HouseModel


@register(HouseModel)
class CategoryTranslationOptions(TranslationOptions):
    fields = ['title', 'descriptions']
