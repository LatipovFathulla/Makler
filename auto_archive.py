from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from products.models import HouseModel


class Command(BaseCommand):
    help = 'Changes the status of the product to inactive after 30 days'

    def handle(self, *args, **kwargs):
        now = timezone.now()
        products = HouseModel.objects.filter(created_at__lte=now - timedelta(days=30))
        products.update(product_status=3)
