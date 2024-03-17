from django.http import HttpResponseRedirect
from django.shortcuts import render
from pathlib import Path

from .models import UploadedFile
from .forms import UploadFileForm

def handle_uploaded_file(f):
    file_path = Path("user_files") / f.name
    with open(file_path, "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def welcome(request):
    return render(request, 'web/welcome.html')

def upload(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            tmp_file = request.FILES["file"]
            instance = UploadedFile(
                name=tmp_file.name,
                file=tmp_file,
                media_type=tmp_file.content_type
            )
            instance.save()
            return HttpResponseRedirect("/upload/")
    else:
        uploaded_files = UploadedFile.objects.all
        form = UploadFileForm()
        context = {
            "uploaded_files": uploaded_files,
            "form": form,
        }
    return render(request, "web/upload.html", context)


def download(request):
    return render(request, "web/download.html")
