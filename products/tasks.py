#
# from celery import shared_task
# from django.utils import timezone
#
# from products.models import HouseModel
#
#
# @shared_task
# def change_model_field():
#     now = timezone.now()
#     thirty_days_ago = now - timezone.timedelta(minutes=1)
#     HouseModel.objects.filter(created_at__lte=thirty_days_ago).update(product_status=3)
#
#

from celery import shared_task
from datetime import timedelta
from django.utils import timezone
from .models import HouseModel


@shared_task(run_every=timedelta(days=30))
def update_product_status():
    products = HouseModel.objects.all()
    for product in products:
        if product.product_status == 0 and product.created_at < timezone.now() - timedelta(days=30):
            product.product_status = 3
            product.save()
