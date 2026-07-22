import shutil
import cv2
import os


def extract_frames(video_path):

    output_folder = "../outputs/frames"

    if os.path.exists(output_folder):
        shutil.rmtree(output_folder)

    os.makedirs(output_folder, exist_ok=True)

    video = cv2.VideoCapture(video_path)

    fps = video.get(cv2.CAP_PROP_FPS)

    # Extract one frame every 5 seconds
    frame_interval = int(fps * 5)

    count = 0
    saved = 0

    while True:

        success, frame = video.read()

        if not success:
            break

        if count % frame_interval == 0:

            frame_path = os.path.join(
                output_folder,
                f"frame_{saved}.jpg"
            )

            cv2.imwrite(frame_path, frame)

            saved += 1

        count += 1

    video.release()

    print(f"Total Frames Saved: {saved}")

    return output_folder