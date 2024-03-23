import subprocess
from datetime import timedelta
from django_q.tasks import async_task, result
from web.models import UploadedFile
import whisperx


def calculate_duration(uploaded_file_id: int):
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


def calculate_transcript(uploaded_file_id: int):
    f = UploadedFile.objects.get(id=uploaded_file_id)
    file_path = f.file.path

    device = "cpu"
    batch_size = 4
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


def process_duration(uploaded_file_id: int):
    """Interface for calculate_duration"""
    async_task(calculate_duration, uploaded_file_id)


def process_transcript(uploaded_file_id: int):
    """Interface for calculate_transcript"""
    async_task(calculate_transcript, uploaded_file_id)
