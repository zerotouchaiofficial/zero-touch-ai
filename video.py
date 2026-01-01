import os
from moviepy.editor import ColorClip, AudioFileClip

# ---------- CONFIG ----------
VIDEO_DIR = "videos"
OUTPUT_VIDEO = os.path.join(VIDEO_DIR, "output.mp4")
AUDIO_FILE = "voice.mp3"
DURATION = 8  # seconds (Shorts safe)
RESOLUTION = (1080, 1920)  # Vertical Shorts
# ----------------------------

def ensure_dirs():
    if not os.path.exists(VIDEO_DIR):
        os.makedirs(VIDEO_DIR)

def create_video():
    if not os.path.exists(AUDIO_FILE):
        print("voice.mp3 not found")
        return

    ensure_dirs()

    audio = AudioFileClip(AUDIO_FILE)
    duration = min(audio.duration, DURATION)

    video = (
        ColorClip(size=RESOLUTION, color=(0, 0, 0))
        .set_duration(duration)
        .set_audio(audio)
    )

    video.write_videofile(
        OUTPUT_VIDEO,
        fps=30,
        codec="libx264",
        audio_codec="aac",
        threads=4,
        verbose=False,
        logger=None
    )

    print("Video created:", OUTPUT_VIDEO)

if __name__ == "__main__":
    create_video()
