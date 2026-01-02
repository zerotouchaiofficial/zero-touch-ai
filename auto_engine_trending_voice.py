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
