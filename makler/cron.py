
from django.utils import timezone
from products.models import HouseModel


def my_new_cron():
    products = HouseModel.objects.all()
    print(products)
    for product in products:
        product.status = 3
        product.created_at = timezone.now()
        product.save()
