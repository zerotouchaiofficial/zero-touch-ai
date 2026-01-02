from fact_engine import get_facts
from voice import make_voice
from video import make_video
from upload import upload_video
import random

TOPICS = [
    "Space", "AI", "Human Brain", "History", "Science",
    "Psychology", "Universe", "Technology"
]

for i in range(20):
    topic = random.choice(TOPICS)

    facts = get_facts(topic)
    script = " ".join(facts)

    audio = make_voice(script)
    video = make_video(audio, facts)

    upload_video(video, topic)

    print(f"✅ Uploaded short {i+1}/20")
