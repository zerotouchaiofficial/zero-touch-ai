import os
from moviepy.editor import ColorClip, AudioFileClip

AUDIO_DIR = "audio"
VIDEO_DIR = "videos"

# Auto-create folders
os.makedirs(AUDIO_DIR, exist_ok=True)
os.makedirs(VIDEO_DIR, exist_ok=True)

audio_files = sorted(os.listdir(AUDIO_DIR))

if not audio_files:
    raise Exception("No audio files found in audio/ — voice.py failed")

audio_path = os.path.join(AUDIO_DIR, audio_files[-1])
audio = AudioFileClip(audio_path)

# Ensure minimum Shorts-safe duration (>= 7s)
duration = max(7, int(audio.duration))

video = (
    ColorClip(size=(720, 1280), color=(0, 0, 0))
    .set_duration(duration)
    .set_audio(audio)
)

output_path = os.path.join(VIDEO_DIR, "short.mp4")

video.write_videofile(
    output_path,
    fps=30,
    codec="libx264",
    audio_codec="aac",
    bitrate="3000k",
)

print(f"Video created: {output_path}")
