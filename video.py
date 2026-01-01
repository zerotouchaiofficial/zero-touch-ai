import os
from moviepy.editor import (
    AudioFileClip,
    ColorClip,
    ImageClip,
    CompositeVideoClip
)

# -------- CONFIG --------
AUDIO_DIR = "audio"
VIDEO_DIR = "videos"
OUTPUT_VIDEO = os.path.join(VIDEO_DIR, "short.mp4")

WIDTH = 1080
HEIGHT = 1920
DURATION = 10  # seconds (YouTube Shorts safe)
FPS = 30
# ------------------------

os.makedirs(VIDEO_DIR, exist_ok=True)

# -------- LOAD AUDIO --------
audio_files = [f for f in os.listdir(AUDIO_DIR) if f.endswith(".mp3")]
if not audio_files:
    raise Exception("No audio files found in audio/ — voice.py failed")

audio_path = os.path.join(AUDIO_DIR, audio_files[0])
audio = AudioFileClip(audio_path)

# Force minimum duration
if audio.duration < DURATION:
    audio = audio.set_duration(DURATION)

# -------- BACKGROUND --------
background = ColorClip(
    size=(WIDTH, HEIGHT),
    color=(15, 15, 15),
    duration=DURATION
)

# -------- OPTIONAL IMAGE OVERLAY --------
image_path = "background.png"
clips = [background]

if os.path.exists(image_path):
    image = (
        ImageClip(image_path)
        .resize(height=HEIGHT)
        .set_duration(DURATION)
        .set_position("center")
    )
    clips.append(image)

# -------- FINAL VIDEO --------
final = CompositeVideoClip(clips)
final = final.set_audio(audio)

final.write_videofile(
    OUTPUT_VIDEO,
    fps=FPS,
    codec="libx264",
    audio_codec="aac",
    bitrate="4000k",
    threads=4,
    preset="medium"
)

print(f"✅ Video created: {OUTPUT_VIDEO}")
