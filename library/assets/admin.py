from django.contrib import admin

# Register your models here.
from library.assets.models import Image


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    fields = ["id", "name", "data"]
    readonly_fields = fields