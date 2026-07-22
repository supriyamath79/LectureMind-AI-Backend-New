import whisper
import os

model = whisper.load_model("tiny")


def transcribe_audio(audio_path):

    print("=" * 50)
    print("Audio Path:", audio_path)
    print("Exists:", os.path.exists(audio_path))
    print("Size:", os.path.getsize(audio_path))
    print("=" * 50)

    result = model.transcribe(audio_path)

    output_folder = "../outputs/transcripts"
    os.makedirs(output_folder, exist_ok=True)

    transcript_name = os.path.splitext(
        os.path.basename(audio_path)
    )[0] + ".txt"

    transcript_path = os.path.join(
        output_folder,
        transcript_name
    )

    with open(transcript_path, "w", encoding="utf-8") as f:
        f.write(result["text"])

    return transcript_path