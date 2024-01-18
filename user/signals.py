# user/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction

from user.models import CustomUser
from payme.models import MerchantTransactionsModel
import logging

logger = logging.getLogger(__name__)



@receiver(post_save, sender=MerchantTransactionsModel)
@transaction.atomic
def update_user_balance(sender, instance, created, **kwargs):
    if created:
        user_id = instance.user_id
        amount = instance.amount

        user, _ = CustomUser.objects.get_or_create(id=user_id)
        user.balance += amount
        user.save()

        logger.info(f"User {user_id} balance updated. New balance: {user.balance}")
