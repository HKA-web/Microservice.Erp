from django.conf import settings as djangosettings
from django.db import models
from django.utils.translation import gettext_lazy as _

from authentication import settings


class OutstandingToken(models.Model):
    id = models.BigAutoField(primary_key=True, serialize=False)
    user = models.ForeignKey(
        djangosettings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )

    jti = models.CharField(unique=True, max_length=255)
    token = models.TextField()

    created_at = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField()

    class Meta:
        db_table = u'\"{}\".\"outstanding_token\"'.format(settings.SCHEMA)
        verbose_name = _('Used store outstanding token')
        abstract = (
            'library.restframeworkjwt.blacklist' not in djangosettings.INSTALLED_APPS
        )
        ordering = ("user",)

    def __str__(self) -> str:
        return "Token for {} ({})".format(
            self.user,
            self.jti,
        )


class BlacklistedToken(models.Model):
    id = models.BigAutoField(primary_key=True, serialize=False)
    token = models.OneToOneField(OutstandingToken, on_delete=models.CASCADE)

    blacklisted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = u'\"{}\".\"blacklisted_token\"'.format(settings.SCHEMA)
        verbose_name = _('Used store blacklisted token')
        abstract = (
            'library.restframeworkjwt.blacklist' not in djangosettings.INSTALLED_APPS
        )

    def __str__(self) -> str:
        return f"Blacklisted token for {self.token.user}"
