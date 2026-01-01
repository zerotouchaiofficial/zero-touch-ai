import os
from moviepy.editor import (
    AudioFileClip,
    ColorClip,
    ImageClip,
    CompositeVideoClip
)

# ---------------- CONFIG ----------------
AUDIO_DIR = "audio"
VIDEO_DIR = "videos"
OUTPUT = os.path.join(VIDEO_DIR, "short.mp4")

WIDTH = 1080
HEIGHT = 1920
DURATION = 10
FPS = 30
# ---------------------------------------

os.makedirs(VIDEO_DIR, exist_ok=True)

# -------- AUDIO --------
audio_files = [f for f in os.listdir(AUDIO_DIR) if f.endswith(".mp3")]
if not audio_files:
    raise Exception("voice.py failed — no audio generated")

audio = AudioFileClip(os.path.join(AUDIO_DIR, audio_files[0]))

if audio.duration < DURATION:
    audio = audio.set_duration(DURATION)

# -------- BACKGROUND --------
background = ColorClip(
    size=(WIDTH, HEIGHT),
    color=(10, 10, 10),
    duration=DURATION
)

clips = [background]

# -------- IMAGE OVERLAY (NO RESIZE) --------
if os.path.exists("background.png"):
    img = (
        ImageClip("background.png")
        .set_duration(DURATION)
        .set_position("center")
    )
    clips.append(img)

# -------- COMPOSE --------
final = CompositeVideoClip(clips, size=(WIDTH, HEIGHT))
final = final.set_audio(audio)

final.write_videofile(
    OUTPUT,
    fps=FPS,
    codec="libx264",
    audio_codec="aac",
    bitrate="5000k",
    preset="medium",
    threads=4
)

print("✅ FINAL VIDEO CREATED:", OUTPUT)
