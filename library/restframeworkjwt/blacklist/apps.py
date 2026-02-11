from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class TokenBlacklistConfig(AppConfig):
    name = "restframeworkjwt.blacklist"
    verbose_name = _("Token Blacklist")
    default_auto_field = "django.db.models.BigAutoField"
