from django.db import models

class UploadedFile(models.Model):
    name = models.CharField(max_length=200)
    file = models.FileField(upload_to="user_files/")
    media_type = models.CharField(max_length=200)

    def __str__(self):
        return self.name
