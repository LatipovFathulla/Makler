from turtle import title

from modeltranslation.translator import register, TranslationOptions

from products.models import HouseModel, CategoryModel


@register(CategoryModel)
class CategoryTranslationOptions(TranslationOptions):
    fields = ['title', 'subtitle']


@register(HouseModel)
class HouseTranslationOptions(TranslationOptions):
    fields = ['title', 'descriptions']
