import subprocess
from datetime import timedelta
from celery import shared_task

from web.models import UploadedFile, Transcript

@shared_task
def add(x, y):
    return x + y


@shared_task
def mul(x, y):
    return x * y


@shared_task
def xsum(numbers):
    return sum(numbers)


@shared_task
def count_transcripts():
    return Transcript.objects.count()


@shared_task
def set_transcript_language(transcript_id, language):
    t = Transcript.objects.get(id=transcript_id)
    t.language = language
    t.save()


@shared_task
def get_duration(uploaded_file_id: int):
    f = UploadedFile.objects.get(id=uploaded_file_id)
    file_path = f.file.path
    p = subprocess.run(['ffprobe',
                        '-v', 'error',
                        '-show_entries', 'format=duration',
                        '-of', 'default=noprint_wrappers=1:nokey=1',
                        file_path],
                        capture_output=True, text=True)
    output = p.stdout
    seconds = float(output)
    duration = timedelta(seconds=seconds)
    f.duration = duration
    f.save()


@shared_task
def get_transcript(uploaded_file_id: int):
    import whisperx  # Import it here because it takes a long time.

    f = UploadedFile.objects.get(id=uploaded_file_id)
    file_path = f.file.path

    device = "cpu"
    batch_size = 16
    compute_type = "float32"
    model = whisperx.load_model("large-v3", device, compute_type=compute_type)
    audio = whisperx.load_audio(file_path)
    result = model.transcribe(audio, batch_size=batch_size)

    language = result["language"]
    model_a, metadata = whisperx.load_align_model(
        language_code=language, device=device)
    result = whisperx.align(result["segments"], model_a, metadata, audio,
                            device, return_char_alignments=False)

    f.transcript_set.create(content=result, language=language)
