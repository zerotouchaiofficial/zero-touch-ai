import os, json, random, pickle
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import ImageSequenceClip, AudioFileClip
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import pyttsx3

# ---------------- BASIC CONFIG ----------------
WIDTH, HEIGHT = 720, 1280
FPS = 30
DURATION = 60
VIDEO_PATH = "videos/short.mp4"
AUDIO_PATH = "videos/voice.wav"
TOKEN_FILE = "youtube_token.pkl"
USED_FACTS_FILE = "used_facts.json"

os.makedirs("videos", exist_ok=True)

# ---------------- TRENDING FACT ENGINE ----------------
TRENDING_FACTS = [
    "NASA confirmed that space has a smell like burning metal",
    "Elon Musk says AI will be smarter than humans very soon",
    "Scientists found a planet where it rains diamonds",
    "Your phone listens for wake words even when locked",
    "The human brain can predict the future milliseconds ahead",
    "Japan created roads that charge electric cars wirelessly",
    "Google knows your location even with GPS off",
    "There is a sound that can instantly make people anxious",
    "Time moves slower near massive objects",
    "Your shadow moves faster than light in some cases",
    "Scientists revived cells from a 30,000 year old animal",
    "There is a hidden message in every QR code",
    "AI can now read thoughts with brain signals",
    "The universe may end sooner than expected",
    "Your name affects your career success",
    "There are colors humans cannot see",
    "Your brain edits reality without you knowing",
    "A single photo can reveal your exact location",
    "Sleep deprivation is more dangerous than alcohol",
    "The internet weighs more than you think"
]

# ---------------- USED FACT TRACKING ----------------
if os.path.exists(USED_FACTS_FILE):
    used = json.load(open(USED_FACTS_FILE))
else:
    used = []

available = [f for f in TRENDING_FACTS if f not in used]
if not available:
    raise Exception("All trending facts used")

fact = random.choice(available)
used.append(fact)
json.dump(used, open(USED_FACTS_FILE, "w"))

# ---------------- VOICE GENERATION ----------------
engine = pyttsx3.init()
engine.setProperty("rate", 150)
engine.save_to_file(fact, AUDIO_PATH)
engine.runAndWait()

# ---------------- VIDEO GENERATION ----------------
frames = []
bg_colors = [(15,15,15), (10,30,60), (40,10,50), (0,60,40)]

for i in range(DURATION * FPS):
    img = Image.new("RGB", (WIDTH, HEIGHT), random.choice(bg_colors))
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", 64)
    except:
        font = ImageFont.load_default()

    y_anim = int((HEIGHT/2) + np.sin(i/12)*25)

    text = "TRENDING FACT 🔥\n\n" + fact
    box = draw.multiline_textbbox((0,0), text, font=font, align="center")
    x = (WIDTH - (box[2]-box[0])) // 2

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
    audio_codec="aac"
)

# ---------------- SEO METADATA ----------------
seo_titles = [
    f"This Is Actually Real 😱 {fact}",
    f"No One Talks About This 😨",
    f"Trending Right Now 🔥",
    f"You Were Never Taught This",
    f"This Changes Everything"
]

title = random.choice(seo_titles) + " #shorts"

description = (
    f"🔥 Trending Fact:\n{fact}\n\n"
    "⚡ Watch till end\n"
    "#shorts #trending #ai #facts #viral #knowledge"
)

tags = [
    "shorts","trending","viral shorts","ai","facts",
    "youtube shorts","did you know","technology","science"
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
