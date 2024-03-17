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

    class Meta:
        ordering = ["-upload_date"]
