import os, json, random, pickle
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import ImageSequenceClip
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# ---------------- SETTINGS ----------------
WIDTH, HEIGHT = 720, 1280
FPS = 30
DURATION = 60
VIDEO_PATH = "videos/short.mp4"
TOKEN_FILE = "youtube_token.pkl"
USED_FACTS_FILE = "used_facts.json"

os.makedirs("videos", exist_ok=True)

# ---------------- FACT DATABASE ----------------
FACT_POOL = [
    "Octopuses have three hearts and blue blood",
    "Honey never spoils even after thousands of years",
    "Bananas are berries but strawberries are not",
    "Sharks existed before trees",
    "Your brain uses 20 percent of your body energy",
    "A day on Venus is longer than a year on Venus",
    "Wombat poop is cube shaped",
    "Butterflies remember being caterpillars",
    "Hot water freezes faster than cold water",
    "Your bones are stronger than steel",
    "There are more stars than grains of sand",
    "The human body glows faintly",
    "Pineapples are berries",
    "An octopus has nine brains",
    "Mosquitoes are attracted to breath",
    "Your heart beats over 100,000 times a day",
    "Water can boil and freeze at same time",
    "The Eiffel Tower grows in summer",
    "Humans share DNA with bananas",
    "Cats can taste air"
]

# ---------------- USED FACT TRACKER ----------------
if os.path.exists(USED_FACTS_FILE):
    used = json.load(open(USED_FACTS_FILE))
else:
    used = []

available = [f for f in FACT_POOL if f not in used]
if not available:
    raise Exception("❌ All facts exhausted")

fact = random.choice(available)
used.append(fact)
json.dump(used, open(USED_FACTS_FILE, "w"))

# ---------------- VIDEO GENERATION ----------------
frames = []

bg_colors = [
    (20, 20, 20),
    (10, 30, 60),
    (40, 10, 50),
    (0, 50, 30),
    (60, 30, 10)
]

for i in range(DURATION * FPS):
    bg = random.choice(bg_colors)
    img = Image.new("RGB", (WIDTH, HEIGHT), bg)
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", 64)
    except:
        font = ImageFont.load_default()

    animated_y = int((HEIGHT / 2) + np.sin(i / 15) * 20)

    text = f"Did you know?\n\n{fact}"
    box = draw.multiline_textbbox((0, 0), text, font=font, align="center")
    x = (WIDTH - (box[2] - box[0])) // 2

    draw.multiline_text(
        (x, animated_y),
        text,
        fill="white",
        font=font,
        align="center"
    )

    frames.append(np.array(img))

clip = ImageSequenceClip(frames, fps=FPS)
clip.write_videofile(VIDEO_PATH, codec="libx264", audio=False)

# ---------------- SEO METADATA ----------------
title = f"Did You Know? {fact} 😱 #shorts"
description = (
    f"🔥 Amazing Fact:\n{fact}\n\n"
    "💡 Learn something new every day!\n"
    "#shorts #facts #didyouknow #viral #knowledge"
)

tags = [
    "shorts", "facts", "did you know", "viral shorts",
    "youtube shorts", "amazing facts", "knowledge"
]

# ---------------- YOUTUBE UPLOAD ----------------
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
