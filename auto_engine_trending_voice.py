import os, json, random, pickle, subprocess, textwrap
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import (
    ImageSequenceClip,
    AudioFileClip,
    concatenate_audioclips
)
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# ---------------- CONFIG ----------------
WIDTH, HEIGHT = 720, 1280
FPS = 30
TOTAL_DURATION = 60
FACTS_PER_VIDEO = 4
SECONDS_PER_FACT = TOTAL_DURATION // FACTS_PER_VIDEO

VIDEO_PATH = "videos/short.mp4"
TOKEN_FILE = "youtube_token.pkl"
USED_FACTS_FILE = "used_facts.json"

os.makedirs("videos", exist_ok=True)

# ---------------- FACT DATABASE ----------------
FACTS = [
    "NASA confirmed that space smells like burning metal",
    "Scientists discovered a planet where it rains diamonds",
    "Your brain edits reality without you noticing",
    "AI can read thoughts using brain signals",
    "Time slows near massive objects",
    "There are colors humans cannot see",
    "Your phone listens even when locked",
    "The universe may end sooner than expected",
    "Your shadow can move faster than light",
    "Sleep deprivation is more dangerous than alcohol",
    "Humans glow faintly in the dark",
    "Your name can affect your success",
    "Memory can be altered without you knowing",
    "Reality is delayed inside your brain",
    "The internet has a physical weight",
]

# ---------------- USED FACT TRACKING ----------------
used = json.load(open(USED_FACTS_FILE)) if os.path.exists(USED_FACTS_FILE) else []
available = [f for f in FACTS if f not in used]

if len(available) < FACTS_PER_VIDEO:
    raise Exception("❌ Not enough unused facts left")

selected_facts = random.sample(available, FACTS_PER_VIDEO)
used.extend(selected_facts)
json.dump(used, open(USED_FACTS_FILE, "w"))

# ---------------- VOICE GENERATION ----------------
audio_clips = []

for i, fact in enumerate(selected_facts):
    audio_path = f"videos/voice_{i}.wav"
    subprocess.run(
        ["espeak", "-s", "145", "-p", "40", "-w", audio_path, fact],
        check=True
    )
    audio_clips.append(AudioFileClip(audio_path))

final_audio = concatenate_audioclips(audio_clips)

# ---------------- TEXT DRAW HELPER ----------------
def draw_centered_text(draw, text, font, y):
    lines = textwrap.wrap(text, width=18)
    text_block = "\n".join(lines)
    bbox = draw.multiline_textbbox((0, 0), text_block, font=font, align="center")
    x = (WIDTH - (bbox[2] - bbox[0])) // 2
    draw.multiline_text((x, y), text_block, fill="white", font=font, align="center")

# ---------------- VIDEO FRAMES ----------------
frames = []
bg_colors = [(15,15,15), (30,60,90), (90,30,60), (20,80,60)]

try:
    font = ImageFont.truetype("DejaVuSans-Bold.ttf", 60)
except:
    font = ImageFont.load_default()

for idx, fact in enumerate(selected_facts):
    bg = random.choice(bg_colors)

    for f in range(SECONDS_PER_FACT * FPS):
        img = Image.new("RGB", (WIDTH, HEIGHT), bg)
        draw = ImageDraw.Draw(img)

        # Animated vertical movement
        y = int(HEIGHT * 0.3 + np.sin(f / 10) * 20)

        draw_centered_text(
            draw,
            f"TRENDING FACT #{idx+1}\n\n{fact}",
            font,
            y
        )

        frames.append(np.array(img))

clip = ImageSequenceClip(frames, fps=FPS)
clip = clip.set_audio(final_audio)

clip.write_videofile(
    VIDEO_PATH,
    codec="libx264",
    audio_codec="aac",
    fps=FPS
)

# ---------------- SEO ----------------
title = random.choice([
    "These Facts Are Insane 😱 #shorts",
    "You Were Never Taught This 🤯 #shorts",
    "Trending Facts You Can't Ignore 🔥 #shorts",
    "This Will Change How You Think 🧠 #shorts"
])

description = (
    "🔥 4 TRENDING FACTS IN 60 SECONDS 🔥\n\n" +
    "\n".join(f"- {f}" for f in selected_facts) +
    "\n\n#shorts #trending #facts #viral #ai"
)

tags = [
    "shorts","trending","facts","viral shorts",
    "did you know","ai","science","knowledge"
]

# ---------------- UPLOAD ----------------
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
print("🚀 Uploaded:", response["id"])
