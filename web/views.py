import subprocess
from datetime import timedelta

from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from .models import UploadedFile
from .forms import UploadFileForm

def get_duration(file) -> timedelta:
    filepath = file.temporary_file_path()
    p = subprocess.run(['ffprobe',
                        '-v', 'error',
                        '-show_entries', 'format=duration',
                        '-of', 'default=noprint_wrappers=1:nokey=1',
                        filepath],
                        capture_output=True, text=True)
    output = p.stdout
    seconds = float(output)
    duration = timedelta(seconds=seconds)
    return duration


def welcome(request):
    return render(request, 'web/welcome.html')


def upload(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            tmp_file = request.FILES["file"]
            duration = get_duration(tmp_file)
            instance = UploadedFile(
                name=tmp_file.name,
                file=tmp_file,
                media_type=tmp_file.content_type,
                size=tmp_file.size,
                duration=duration,
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
