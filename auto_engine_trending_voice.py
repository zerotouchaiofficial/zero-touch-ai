import os
import json
import random
import subprocess
import textwrap
import pickle
import numpy as np

from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import (
    ImageSequenceClip,
    AudioFileClip,
    concatenate_audioclips
)
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# ================= CONFIG =================
WIDTH, HEIGHT = 720, 1280
FPS = 30
MAX_DURATION = 60

VIDEO_PATH = "videos/short.mp4"
TOKEN_FILE = "youtube_token.pkl"
USED_FACTS_FILE = "used_facts.json"

os.makedirs("videos", exist_ok=True)

# ================= FACT POOL =================
FACTS = [
    "NASA confirmed that space smells like burning metal",
    "Scientists discovered a planet where it rains diamonds",
    "Your brain edits reality before you see it",
    "There are colors humans cannot perceive",
    "Time moves slower near massive objects",
    "Humans glow faintly due to bioluminescence",
    "Your shadow can move faster than light",
    "The universe may not be infinite",
    "Sleep deprivation is deadlier than alcohol",
    "Your memory can be rewritten without you noticing",
]

used = json.load(open(USED_FACTS_FILE)) if os.path.exists(USED_FACTS_FILE) else []
available = [f for f in FACTS if f not in used]

if len(available) < 3:
    raise Exception("❌ Not enough unused facts left")

random.shuffle(available)

# ================= FONT =================
try:
    font = ImageFont.truetype("DejaVuSans-Bold.ttf", 64)
except:
    font = ImageFont.load_default()

# ================= TEXT DRAW =================
def draw_text(draw, text, frame_index):
    wrapped = textwrap.wrap(text, width=18)
    block = "\n".join(wrapped)

    bbox = draw.multiline_textbbox((0, 0), block, font=font, align="center")
    text_w = bbox[2] - bbox[0]

    # simple floating animation
    y = HEIGHT // 2 - 120 + int(np.sin(frame_index / 8) * 20)
    x = (WIDTH - text_w) // 2

    draw.multiline_text(
        (x, y),
        block,
        fill="white",
        font=font,
        align="center"
    )

# ================= GENERATE VOICE + FRAMES =================
audio_clips = []
frames = []
total_time = 0.0

bg_colors = [
    (15, 15, 15),
    (30, 60, 90),
    (90, 30, 60),
    (20, 80, 60),
]

fact_index = 0

for fact in available:
    if total_time >= MAX_DURATION:
        break

    voice_path = f"videos/voice_{fact_index}.wav"

    subprocess.run(
        ["espeak", "-s", "140", "-p", "45", "-w", voice_path, fact],
        check=True
    )

    audio = AudioFileClip(voice_path)
    duration = audio.duration

    # stop if exceeding 60s
    if total_time + duration > MAX_DURATION:
        duration = MAX_DURATION - total_time
        audio = audio.subclip(0, duration)

    audio_clips.append(audio)

    frame_count = int(duration * FPS)
    bg = bg_colors[fact_index % len(bg_colors)]

    for f in range(frame_count):
        img = Image.new("RGB", (WIDTH, HEIGHT), bg)
        draw = ImageDraw.Draw(img)

        draw_text(
            draw,
            f"FACT #{fact_index + 1}\n\n{fact}",
            f
        )

        frames.append(np.array(img))

    total_time += duration
    used.append(fact)
    fact_index += 1

json.dump(used, open(USED_FACTS_FILE, "w"))

# ================= FINAL VIDEO =================
final_audio = concatenate_audioclips(audio_clips)
final_audio = final_audio.set_duration(min(final_audio.duration, MAX_DURATION))

clip = ImageSequenceClip(frames, fps=FPS)
clip = clip.set_audio(final_audio)

clip.write_videofile(
    VIDEO_PATH,
    codec="libx264",
    audio_codec="aac",
    fps=FPS,
    threads=2
)

# ================= SEO =================
title = random.choice([
    "These Facts Will Blow Your Mind 😱 #shorts",
    "60 Seconds of Insane Facts 🤯 #shorts",
    "You Were Never Taught This 🔥 #shorts",
])

description = (
    "🔥 TRENDING FACTS IN 60 SECONDS 🔥\n\n"
    + "\n".join(f"• {f}" for f in used[-fact_index:])
    + "\n\n#shorts #trending #facts #viral #science"
)

tags = [
    "shorts", "trending", "facts", "viral",
    "did you know", "science", "mind blowing"
]

# ================= UPLOAD =================
creds = pickle.load(open(TOKEN_FILE, "rb"))
youtube = build("youtube", "v3", credentials=creds)

request = youtube.videos().insert(
    part="snippet,status",
    body={
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags,
            "categoryId": "22"
        },
        "status": {"privacyStatus": "public"}
    },
    media_body=MediaFileUpload(VIDEO_PATH, mimetype="video/mp4", resumable=True)
)

response = request.execute()
print("🚀 Uploaded Short:", response["id"])
