from django.contrib import admin

from library.users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["id", "first_name", "last_name", "email", "verified_on"]