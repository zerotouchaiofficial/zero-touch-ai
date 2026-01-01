import os
from moviepy.editor import ColorClip, AudioFileClip, concatenate_audioclips

AUDIO_DIR = "audio"
VIDEO_DIR = "videos"
OUTPUT_VIDEO = os.path.join(VIDEO_DIR, "short.mp4")

# Always create folders (GitHub Actions safe)
os.makedirs(AUDIO_DIR, exist_ok=True)
os.makedirs(VIDEO_DIR, exist_ok=True)

audio_files = sorted([
    f for f in os.listdir(AUDIO_DIR)
    if f.endswith(".mp3")
])

if not audio_files:
    raise Exception("No audio files found in audio/ — voice.py failed")

audio_clips = []
for file in audio_files:
    audio_clips.append(AudioFileClip(os.path.join(AUDIO_DIR, file)))

final_audio = concatenate_audioclips(audio_clips)

duration = final_audio.duration

# Create vertical Shorts video (1080x1920)
clip = ColorClip(
    size=(1080, 1920),
    color=(0, 0, 0),
    duration=duration
).set_audio(final_audio)

clip.write_videofile(
    OUTPUT_VIDEO,
    fps=30,
    codec="libx264",
    audio_codec="aac",
    preset="medium"
)

print("Video created:", OUTPUT_VIDEO)
