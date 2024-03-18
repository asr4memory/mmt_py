from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from pathlib import Path

from .models import UploadedFile
from .forms import UploadFileForm


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
                media_type=tmp_file.content_type,
                size=tmp_file.size,
            )
            instance.save()
            return HttpResponseRedirect("/uploaded-files/")
    else:
        form = UploadFileForm()
    return render(request, "web/upload.html", {"form": form})


def uploaded_files(request):
    uploaded_files = UploadedFile.objects.all
    context = {"uploaded_files": uploaded_files}
    return render(request, "web/uploaded_files.html", context)


def uploaded_file_detail(request, file_id):
    uploaded_file = get_object_or_404(UploadedFile, id=file_id)
    context = {"uploaded_file": uploaded_file}
    return render(request, "web/uploaded_file_detail.html", context)


def download(request):
    return render(request, "web/download.html")
