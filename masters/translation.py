from modeltranslation.translator import register, TranslationOptions

from masters.models import MasterProfessionModel, HowServiceModel, MasterModel


@register(MasterProfessionModel)
class MasterProfessionModelOptions(TranslationOptions):
    fields = ['title']


@register(HowServiceModel)
class HowServiceModelOptions(TranslationOptions):
    fields = ['title']


@register(MasterModel)
class MasterModelOptions(TranslationOptions):
    fields = ['name', 'descriptions']
