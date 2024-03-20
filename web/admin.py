from django.contrib import admin
from web.models import UploadedFile, Transcript


@admin.register(UploadedFile)
class UploadedFileAdmin(admin.ModelAdmin):
    date_hierarchy = "upload_date"


@admin.register(Transcript)
class TranscriptAdmin(admin.ModelAdmin):
    pass
