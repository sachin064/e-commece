from django.contrib import admin
from .models import User

# Register your models here.
from django.contrib.auth.admin import UserAdmin


class UserAdmin(UserAdmin):
    pass


admin.site.register(User, UserAdmin)
