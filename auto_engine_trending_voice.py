import os, json, random, subprocess, textwrap, pickle
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import ImageSequenceClip, AudioFileClip, concatenate_audioclips
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# ================== CONFIG ==================
WIDTH, HEIGHT = 720, 1280
FPS = 30
TOTAL_DURATION = 60
FACTS_PER_VIDEO = 4
SECONDS_PER_FACT = TOTAL_DURATION // FACTS_PER_VIDEO

VIDEO_PATH = "videos/short.mp4"
TOKEN_FILE = "youtube_token.pkl"
USED_FACTS_FILE = "used_facts.json"

os.makedirs("videos", exist_ok=True)

# ================== FACT POOL ==================
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

if len(available) < FACTS_PER_VIDEO:
    raise Exception("❌ Not enough unused facts")

selected_facts = random.sample(available, FACTS_PER_VIDEO)
used.extend(selected_facts)
json.dump(used, open(USED_FACTS_FILE, "w"))

# ================== VOICE (SYNCED) ==================
audio_clips = []

for i, fact in enumerate(selected_facts):
    audio_path = f"videos/voice_{i}.wav"
    subprocess.run(
        ["espeak", "-s", "140", "-p", "45", "-w", audio_path, fact],
        check=True
    )
    clip = AudioFileClip(audio_path).set_duration(SECONDS_PER_FACT)
    audio_clips.append(clip)

final_audio = concatenate_audioclips(audio_clips)

# ================== FONT ==================
try:
    font = ImageFont.truetype("DejaVuSans-Bold.ttf", 64)
except:
    font = ImageFont.load_default()

# ================== TEXT DRAW ==================
def draw_fact(draw, text, frame_idx):
    wrapped = textwrap.wrap(text, width=18)
    block = "\n".join(wrapped)

    bbox = draw.multiline_textbbox((0, 0), block, font=font, align="center")
    text_w = bbox[2] - bbox[0]

    # TEXT ANIMATION (slide up + fade illusion)
    base_y = HEIGHT // 2 - 100
    anim_offset = int(np.sin(frame_idx / 8) * 20)
    x = (WIDTH - text_w) // 2
    y = base_y + anim_offset

    draw.multiline_text((x, y), block, fill="white", font=font, align="center")

# ================== VIDEO FRAMES ==================
frames = []
bg_colors = [
    (15, 15, 15),
    (30, 60, 90),
    (90, 30, 60),
    (20, 80, 60)
]

for fact_index, fact in enumerate(selected_facts):
    bg = bg_colors[fact_index % len(bg_colors)]

    for f in range(SECONDS_PER_FACT * FPS):
        img = Image.new("RGB", (WIDTH, HEIGHT), bg)
        draw = ImageDraw.Draw(img)

        draw_fact(draw, f"FACT #{fact_index+1}\n\n{fact}", f)

        frames.append(np.array(img))

clip = ImageSequenceClip(frames, fps=FPS)
clip = clip.set_audio(final_audio)

clip.write_videofile(
    VIDEO_PATH,
    codec="libx264",
    audio_codec="aac",
    fps=FPS,
    threads=2
)

# ================== SEO ==================
title = random.choice([
    "4 Facts That Will Blow Your Mind 😱 #shorts",
    "These 60 Seconds Will Change You 🤯 #shorts",
    "You Were Never Taught This 🔥 #shorts",
])

description = (
    "🔥 4 TRENDING FACTS IN 60 SECONDS 🔥\n\n" +
    "\n".join(f"• {f}" for f in selected_facts) +
    "\n\n#shorts #trending #facts #viral #science #ai"
)

tags = [
    "shorts","trending","facts","viral","science",
    "did you know","mind blowing","ai"
]

# ================== UPLOAD ==================
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
