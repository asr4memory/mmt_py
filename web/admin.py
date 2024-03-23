from typing import Any
import os
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http import HttpRequest
from web.models import UploadedFile, Transcript


@admin.register(UploadedFile)
class UploadedFileAdmin(admin.ModelAdmin):
    list_display = ["name", "media_type", "size", "duration", "upload_date"]

    def delete_queryset(self, request: HttpRequest, queryset: QuerySet[Any]) -> None:
        for uploaded_file in queryset:
            os.remove(uploaded_file.file.path)
        super(UploadedFileAdmin, self).delete_queryset(request, queryset)


@admin.register(Transcript)
class TranscriptAdmin(admin.ModelAdmin):
    list_display = ["uploaded_file", "language"]
