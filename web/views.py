import subprocess
from datetime import timedelta

from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from web.models import UploadedFile, Transcript
from web.forms import UploadFileForm


def get_duration(filepath: str) -> timedelta:
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

def get_transcript(filepath: str) -> dict:
    import whisperx  # Import it here because it takes a long time.
    device = "cpu"
    batch_size = 16
    compute_type = "float32"
    model = whisperx.load_model("large-v3", device, compute_type=compute_type)
    audio = whisperx.load_audio(filepath)
    result = model.transcribe(audio, batch_size=batch_size)

    language = result["language"]
    model_a, metadata = whisperx.load_align_model(
        language_code=language, device=device)
    result = whisperx.align(result["segments"], model_a, metadata, audio,
                            device, return_char_alignments=False)
    return (result, language);


def welcome(request):
    return render(request, 'web/welcome.html')


def upload(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            tmp_file = request.FILES["file"]
            duration = get_duration(tmp_file.temporary_file_path())
            instance = UploadedFile(
                name=tmp_file.name,
                file=tmp_file,
                media_type=tmp_file.content_type,
                size=tmp_file.size,
                duration=duration,
            )
            instance.save()

            transcript, language = get_transcript(instance.file.path)
            instance.transcript_set.create(content=transcript,
                                           language=language)

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


def download(request):
    return render(request, "web/download.html")
