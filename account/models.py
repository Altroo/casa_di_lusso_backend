from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_("Adresse e-mail"), unique=True)
    first_name = models.CharField(_("Prénom"), max_length=30, blank=True)
    last_name = models.CharField(_("Nom"), max_length=30, blank=True)
    is_staff = models.BooleanField(_("Statut personnel"), default=False, db_index=True)
    is_active = models.BooleanField(_("Actif"), default=True, db_index=True)
    date_joined = models.DateTimeField(_("Date d'inscription"), default=timezone.now, db_index=True)
    date_updated = models.DateTimeField(_("Date de modification"), auto_now=True, db_index=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name = _("Utilisateur")
        verbose_name_plural = _("Utilisateurs")
        ordering = ("-date_joined",)

    def __str__(self):
        return self.get_full_name() or self.email

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    def get_short_name(self):
        return self.first_name or self.email
