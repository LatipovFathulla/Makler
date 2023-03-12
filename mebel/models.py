from django.db import models
from django.utils.translation import gettext_lazy as _

from products.models import PriceListModel


class MebelCategoryModel(models.Model):
    title = models.CharField(max_length=250, verbose_name=_('title'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created_at'))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Mebel_Category')
        verbose_name_plural = _('Mebel_Categories')


class MebelModel(models.Model):
    creator = models.ForeignKey('user.CustomUser', on_delete=models.CASCADE, related_name='mebels', null=True)
    title = models.CharField(max_length=400, verbose_name=_('title'))
    category = models.ForeignKey(MebelCategoryModel, on_delete=models.CASCADE, null=True)
    price = models.IntegerField(verbose_name=_('price'), null=True)
    phone_number = models.IntegerField(verbose_name=_('phone_number'), null=True)
    web_address_title = models.CharField(max_length=400, verbose_name=_('web_address_title'), null=True)
    web_address_latitude = models.FloatField(verbose_name=_('web_address_latitude'), null=True)
    web_address_longtitude = models.FloatField(verbose_name=_('web_address_longtitude'), null=True)
    price_type = models.ForeignKey(PriceListModel, on_delete=models.CASCADE, related_name='price_types_mebel', null=True)
    short_descriptions = models.TextField(verbose_name=_('short_descriptions'), null=True)
    long_descriptions = models.TextField(verbose_name=_('descriptions'), null=True)
    draft = models.BooleanField(default=False, null=True)
    view_count = models.PositiveIntegerField(default=0, null=True)
    PRODUCT_STATUS = [
        (0, 'InProgress'),
        (1, 'PUBLISH'),
        (2, 'DELETED'),
        (3, 'ARCHIVED'),
        (4, 'REJECTED'),
    ]
    product_status = models.IntegerField(
        choices=PRODUCT_STATUS,
        default=0,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Mebel')
        verbose_name_plural = _('Mebels')


class NewMebelImages(models.Model):
    product = models.ForeignKey(MebelModel, on_delete=models.CASCADE, related_name='images')
    images = models.ImageField(upload_to='API/mebel/images', max_length=100, null=True)
