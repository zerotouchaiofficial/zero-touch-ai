import os, json, random, subprocess, requests, tempfile
from moviepy.editor import (
    VideoFileClip, AudioFileClip, CompositeVideoClip,
    ImageSequenceClip, ColorClip
)
from PIL import Image, ImageDraw, ImageFont
import numpy as np

WIDTH, HEIGHT = 1080, 1920
FPS = 30
FACTS_PER_VIDEO = 4
VOICE = "en-IN-NeerjaNeural"
USED_FACTS_FILE = "data/used_facts.json"

os.makedirs("data", exist_ok=True)
os.makedirs("videos", exist_ok=True)

# ---------------- SAFE FACTS ---------------- #

OFFLINE_FACTS = [
    "Octopuses have three hearts and blue blood.",
    "Bananas are berries, but strawberries are not.",
    "A day on Venus is longer than a year on Venus.",
    "Honey never spoils, even after thousands of years.",
    "Sharks existed before trees.",
    "Wombat poop is cube-shaped.",
    "There are more stars in the universe than grains of sand on Earth.",
    "The Eiffel Tower grows about 6 inches in summer."
]

def fetch_fact():
    try:
        r = requests.get(
            "https://uselessfacts.jsph.pl/random.json?language=en",
            timeout=5
        )
        return r.json().get("text", "").strip()
    except Exception:
        return random.choice(OFFLINE_FACTS)

def get_new_facts(count):
    with open(USED_FACTS_FILE) as f:
        used = set(json.load(f))

    facts = []
    tries = 0

    while len(facts) < count and tries < 50:
        fact = fetch_fact()
        if fact and fact not in used and len(fact) < 140:
            facts.append(fact)
            used.add(fact)
        tries += 1

    with open(USED_FACTS_FILE, "w") as f:
        json.dump(list(used), f, indent=2)

    return facts

# ---------------- BULLETPROOF BACKGROUND ---------------- #

def download_background():
    urls = [
        "https://cdn.pixabay.com/video/2023/05/06/161079-824274089_large.mp4",
        "https://cdn.pixabay.com/video/2022/10/10/134254-758746924_large.mp4",
        "https://cdn.pixabay.com/video/2023/03/29/157230-812991593_large.mp4"
    ]

    for url in urls:
        try:
            tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
            with requests.get(url, stream=True, timeout=15) as r:
                if r.status_code != 200:
                    continue
                for chunk in r.iter_content(chunk_size=8192):
                    tmp.write(chunk)
            tmp.close()

            # size check (must be > 1MB)
            if os.path.getsize(tmp.name) > 1_000_000:
                return tmp.name
        except Exception:
            pass

    # FINAL FAILSAFE: animated solid background
    return None

def fallback_background(duration):
    return ColorClip(
        size=(WIDTH, HEIGHT),
        color=(20, 20, 20),
        duration=duration
    )

# ---------------- VOICE ---------------- #

def generate_voice(text, output):
    subprocess.run([
        "edge-tts",
        "--voice", VOICE,
        "--text", text,
        "--write-media", output
    ], check=True)

# ---------------- TEXT ---------------- #

def render_text(text):
    img = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 70
    )

    words = text.split()
    lines, line = [], ""

    for w in words:
        if draw.textlength(line + w, font=font) < 900:
            line += w + " "
        else:
            lines.append(line)
            line = w + " "
    lines.append(line)

    y = HEIGHT // 2 - len(lines) * 45
    for l in lines:
        draw.text((WIDTH // 2, y), l, fill="white", font=font, anchor="mm")
        y += 90

    return np.array(img)

# ---------------- MAIN ---------------- #

def main():
    facts = get_new_facts(FACTS_PER_VIDEO)

    narration = " ".join([f"Fact. {f}." for f in facts])

    voice_path = "videos/voice.wav"
    generate_voice(narration, voice_path)

    audio = AudioFileClip(voice_path)
    duration = min(60, audio.duration)

    bg_path = download_background()
    if bg_path:
        bg = VideoFileClip(bg_path).resize((WIDTH, HEIGHT)).subclip(0, duration)
    else:
        bg = fallback_background(duration)

    frames = []
    sec_per_fact = duration / len(facts)

    for fact in facts:
        frame = render_text(fact)
        frames.extend([frame] * int(sec_per_fact * FPS))

    txt_clip = ImageSequenceClip(frames, fps=FPS)

    final = CompositeVideoClip([bg, txt_clip.set_position("center")])
    final = final.set_audio(audio)

    final.write_videofile(
        "videos/short.mp4",
        fps=FPS,
        codec="libx264",
        audio_codec="aac"
    )

main()
