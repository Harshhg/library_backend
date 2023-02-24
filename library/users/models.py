from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import CIEmailField
from django.db import models

from library.assets.models import Image


class User(AbstractUser):
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    email = CIEmailField(unique=True, db_index=True)
    verified_on = models.DateTimeField(null=True)
    verification_id = models.OneToOneField(Image, on_delete=models.PROTECT, null=True)

    REQUIRED_FIELDS = ["email"]

    def is_verified(self):
        return bool(self.verified_on)
