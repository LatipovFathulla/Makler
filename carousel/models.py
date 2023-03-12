from django.db import models
from django.utils.translation import gettext_lazy as _


class CarouselModel(models.Model):
    image = models.FileField(upload_to='carousel/images', null=True)
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        verbose_name = _('Карусель')
        verbose_name_plural = _('Карусели')

