# user/apps.py
from django.apps import AppConfig

import logging

logger = logging.getLogger(__name__)


class UserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'user'
    verbose_name = 'Пользователи'

    def ready(self):
        import user.signals
        logger.info("Users signals are ready!")
