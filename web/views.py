from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from web.models import UploadedFile, Transcript
from web.forms import UploadFileForm
from web.tasks import get_duration, get_transcript


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
            get_duration.delay(instance.id)
            get_transcript.delay(instance.id)

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
    context = {
        "uploaded_file": uploaded_file,
        "transcripts": uploaded_file.transcript_set.all(),
    }
    return render(request, "web/uploaded_file_detail.html", context)


def transcript_detail(request, transcript_id):
    transcript = get_object_or_404(Transcript, id=transcript_id)
    return render(request, "web/transcript_detail.html",
                  {"transcript": transcript})


def segment_detail(request, transcript_id, segment_index):
    transcript = get_object_or_404(Transcript, id=transcript_id)
    segment = transcript.content["segments"][segment_index - 1]

    start = segment["start"]
    end = segment["end"]
    words = segment["words"]

    factor = 300

    new_words = [{
        "word": word["word"],
        "start": word["start"],
        "end": word["end"],
        "score": word["score"],
        "left": (word["start"] - start) * factor,
        "width": (word["end"] - word["start"]) * factor,
    } for word in words]

    context = {
        "transcript": transcript,
        "segment_index": segment_index,
        "segment": segment,
        "new_words": new_words,
        "width": (end - start) * factor,
    }
    return render(request, "web/segment_detail.html", context)


def download(request):
    return render(request, "web/download.html")
