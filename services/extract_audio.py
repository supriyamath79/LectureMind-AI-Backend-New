import ffmpeg
import os


def extract_audio(video_path):

    output_folder = "../outputs/audio"
    os.makedirs(output_folder, exist_ok=True)

    video_name = os.path.splitext(os.path.basename(video_path))[0]

    audio_path = os.path.join(output_folder, f"{video_name}.wav")

    (
        ffmpeg
        .input(video_path)
        .output(audio_path, acodec="pcm_s16le", ac=1, ar="16000")
        .overwrite_output()
        .run()
    )

    return audio_path