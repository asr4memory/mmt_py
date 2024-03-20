import os
from django.db import models

class UploadedFile(models.Model):
    name = models.CharField(max_length=200)
    file = models.FileField(upload_to="user_files/")
    media_type = models.CharField(max_length=200)
    size = models.IntegerField()
    upload_date = models.DateTimeField(auto_now_add=True)
    duration = models.DurationField(null=True, blank=True)

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        """
        Remove file from disk before deleting record.
        Does not work on bulk operations in Django Admin.
        """
        os.remove(self.file.path)
        super(UploadedFile, self).delete(*args,**kwargs)

    class Meta:
        ordering = ["-upload_date"]


class Transcript(models.Model):
    uploaded_file = models.ForeignKey(UploadedFile, on_delete=models.CASCADE)
    content = models.JSONField()
    language = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.uploaded_file}-{self.language}"
