from modeltranslation.translator import register, TranslationOptions

from mebel.models import MebelCategoryModel, MebelModel


@register(MebelCategoryModel)
class MebelCategoryModelOptions(TranslationOptions):
    fields = ['title']


@register(MebelModel)
class MebelModelOptions(TranslationOptions):
    fields = ['title', 'short_descriptions', 'long_descriptions']
