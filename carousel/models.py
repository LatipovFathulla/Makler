from django.db import models
from django.utils.translation import gettext_lazy as _


class CarouselModel(models.Model):
    image = models.FileField(upload_to='carousel/images', null=True, verbose_name=_('image'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created_at'))

    class Meta:
        verbose_name = _('Карусель')
        verbose_name_plural = _('Карусели')


class BannerADSModel(models.Model):
    image = models.FileField(upload_to='banner_ads/images', null=True, verbose_name=_('banner_ads_image'))
    url = models.URLField(max_length=250, verbose_name=_('url'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('created_at'))

    class Meta:
        verbose_name = _('Banner_ads')
        verbose_name_plural = _('Banner_ads')
