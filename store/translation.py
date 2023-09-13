from modeltranslation.translator import register, TranslationOptions
from .models import StoreAmenities, UseForModel, HowStoreServiceModel, StoreModel


@register(StoreAmenities)
class StoreAmenitiesOptions(TranslationOptions):
    fields = ['title']


@register(UseForModel)
class UseForModelOptions(TranslationOptions):
    fields = ['title']


@register(HowStoreServiceModel)
class HowStoreServiceModelOptions(TranslationOptions):
    fields = ['title']


@register(StoreModel)
class StoreModelOptions(TranslationOptions):
    fields = ['name', 'description']