import os
from moviepy.editor import ImageClip, AudioFileClip

FACTS_DIR = "facts"
AUDIO_DIR = "audio"
VIDEOS_DIR = "videos"

os.makedirs(VIDEOS_DIR, exist_ok=True)

fact_files = sorted(os.listdir(FACTS_DIR))
audio_files = sorted(os.listdir(AUDIO_DIR))

fact = open(os.path.join(FACTS_DIR, fact_files[-1])).read().strip()
audio_path = os.path.join(AUDIO_DIR, audio_files[-1])

audio = AudioFileClip(audio_path)

# Create solid background
clip = ImageClip("background.png").set_duration(audio.duration)
clip = clip.set_audio(audio)

output_path = os.path.join(VIDEOS_DIR, "short.mp4")

clip.write_videofile(
    output_path,
    codec="libx264",
    audio_codec="aac",
    fps=30,
    preset="medium",
    threads=4,
    ffmpeg_params=[
        "-pix_fmt", "yuv420p",
        "-movflags", "+faststart"
    ]
)

print("VIDEO CREATED:", output_path)
