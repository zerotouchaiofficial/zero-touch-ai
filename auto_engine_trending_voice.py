import os, json, random, pickle, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import ImageSequenceClip, AudioFileClip
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# ---------------- CONFIG ----------------
WIDTH, HEIGHT = 720, 1280
FPS = 30
DURATION = 60
VIDEO_PATH = "videos/short.mp4"
AUDIO_PATH = "videos/voice.wav"
TOKEN_FILE = "youtube_token.pkl"
USED_FACTS_FILE = "used_facts.json"

os.makedirs("videos", exist_ok=True)

# ---------------- TRENDING FACTS ----------------
TRENDING_FACTS = [
    "NASA confirmed that space smells like burning metal",
    "Scientists discovered a planet where it rains diamonds",
    "Your brain edits reality without you noticing",
    "AI can now read thoughts using brain signals",
    "Time moves slower near massive objects",
    "There are colors humans cannot see",
    "Your phone listens even when locked",
    "The universe may end sooner than expected",
    "A single photo can reveal your location",
    "Sleep deprivation is more dangerous than alcohol",
    "Your shadow can move faster than light",
    "Google knows your location with GPS off",
    "Humans glow faintly in the dark",
    "Your name can affect your success",
    "There is a sound that causes instant fear",
    "Your brain predicts the future milliseconds ahead",
    "The internet has a physical weight",
    "Memory can be altered without you knowing",
    "Your eyes see things that don’t exist",
    "Reality is delayed inside your brain"
]

# ---------------- USED FACT TRACKING ----------------
if os.path.exists(USED_FACTS_FILE):
    used = json.load(open(USED_FACTS_FILE))
else:
    used = []

available = [f for f in TRENDING_FACTS if f not in used]
if not available:
    raise Exception("❌ All trending facts exhausted")

fact = random.choice(available)
used.append(fact)
json.dump(used, open(USED_FACTS_FILE, "w"))

# ---------------- VOICE (espeak – CI SAFE) ----------------
subprocess.run([
    "espeak",
    "-s", "145",
    "-p", "40",
    "-w", AUDIO_PATH,
    fact
], check=True)

# ---------------- VIDEO GENERATION ----------------
frames = []
bg_colors = [(10,10,10), (20,40,80), (60,20,60), (0,60,40)]

for i in range(DURATION * FPS):
    img = Image.new("RGB", (WIDTH, HEIGHT), random.choice(bg_colors))
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", 64)
    except:
        font = ImageFont.load_default()

    y_anim = int((HEIGHT / 2) + np.sin(i / 14) * 25)

    text = "TRENDING FACT 🔥\n\n" + fact
    box = draw.multiline_textbbox((0, 0), text, font=font, align="center")
    x = (WIDTH - (box[2] - box[0])) // 2

    draw.multiline_text(
        (x, y_anim),
        text,
        fill="white",
        font=font,
        align="center"
    )

    frames.append(np.array(img))

clip = ImageSequenceClip(frames, fps=FPS)
audio = AudioFileClip(AUDIO_PATH)
clip = clip.set_audio(audio)

clip.write_videofile(
    VIDEO_PATH,
    codec="libx264",
    audio_codec="aac",
    fps=FPS
)

# ---------------- SEO ----------------
title_templates = [
    f"This Is Actually Real 😱 #shorts",
    f"No One Talks About This 😨 #shorts",
    f"Trending Right Now 🔥 #shorts",
    f"You Were Never Taught This #shorts",
    f"This Changes Everything 🤯 #shorts"
]

title = random.choice(title_templates)
description = (
    f"🔥 TRENDING FACT:\n{fact}\n\n"
    "#shorts #trending #facts #ai #viral #knowledge"
)

tags = [
    "shorts","trending","viral shorts","facts",
    "did you know","ai","science","technology"
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
print("🚀 Uploaded video ID:", response["id"])
