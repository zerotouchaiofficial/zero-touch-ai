import json, random
from moviepy.editor import (
    ImageClip, AudioFileClip,
    CompositeVideoClip, concatenate_videoclips
)

WIDTH, HEIGHT = 1080, 1920

with open("facts.json") as f:
    facts = json.load(f)

audio = AudioFileClip("voice.mp3")
duration_per_fact = audio.duration / len(facts)

clips = []

for fact in facts:
    bg = random.choice([
        "backgrounds/bg1.jpg",
        "backgrounds/bg2.jpg",
        "backgrounds/bg3.jpg"
    ])

    clip = (
        ImageClip(bg)
        .set_duration(duration_per_fact)
        .resize((WIDTH, HEIGHT))
    )

    clips.append(clip)

video = concatenate_videoclips(clips).set_audio(audio)

video.write_videofile(
    "videos/short.mp4",
    fps=30,
    codec="libx264",
    audio_codec="aac"
)

print("✅ Video created")
