from django.contrib import admin
from web.models import UploadedFile


@admin.register(UploadedFile)
class UploadedFileAdmin(admin.ModelAdmin):
    date_hierarchy = "upload_date"
