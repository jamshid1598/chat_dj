import uuid
from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import gettext_lazy as _
from user.manager import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    username = models.CharField(_('username'), max_length=255, unique=True)
    name = models.CharField(_("Name of User"), blank=True, max_length=255)
    first_name = models.CharField(_('first name'), max_length=255, blank=True, null=True)
    last_name = models.CharField(_('last name'), max_length=255, blank=True, null=True)
    two_step_password = models.BooleanField(_("two step password"), default=False, help_text=_("is active two step password?"))

    is_active = models.BooleanField(_('is_active'), default=True)
    is_staff = models.BooleanField(_('is_staff'), default=False)
    is_superuser = models.BooleanField(_('is_superuser'), default=False)

    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'

    class Meta:
        ordering = ('created_at', 'updated_at')
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)

    @property
    def full_name(self):
        return "%s %s" % (self.first_name, self.last_name)

    def get_absolute_url(self):
        return "/user/%i/" % (self.pk)
