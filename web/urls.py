from django.urls import path

from . import views

app_name = "web"

urlpatterns = [
    path("", views.welcome, name="welcome"),
    path("upload/", views.upload, name="upload"),
    path("uploaded-files/", views.uploaded_files, name="uploaded-files"),
    path("uploaded-files/<int:file_id>/", views.uploaded_file_detail,
         name="uploaded-file-detail"),
    path("transcripts/<int:transcript_id>/", views.transcript_detail,
         name="transcript-detail"),
    path("transcripts/<int:transcript_id>/<int:segment_index>/",
         views.segment_detail, name="segment-detail"),
    path("download/", views.download, name="download"),
    path("queues/", views.queues, name="queues"),
]
