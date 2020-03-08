from django.db import models
from django.utils import timezone

from django.contrib.auth.models import AbstractUser
from .managers import UserManager


# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True)
    is_deleted = models.BooleanField(default=False)
    is_first_login = models.BooleanField(default=False)
    created_on = models.DateTimeField(default=timezone.now)
    updated_on = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='created')
    updated_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='updated')

    REQUIRED_FIELDS = ('email',)
    objects = UserManager()

    def __str__(self):
        return self.username
