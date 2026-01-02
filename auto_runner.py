from fact_engine import get_facts
from voice import generate_voice
from generate_video import generate_video
from upload import upload_video
import random

TOPICS = [
    "Space",
    "Artificial Intelligence",
    "Human Brain",
    "Psychology",
    "History",
    "Science",
    "Universe",
    "Technology"
]

for i in range(20):
    topic = random.choice(TOPICS)

    print(f"▶ Generating short {i+1}/20 on {topic}")

    facts = get_facts(topic)
    script = " ".join(facts)

    audio_path = generate_voice(script)
    video_path = generate_video(audio_path, facts)

    upload_video(video_path, topic)

    print(f"✅ Uploaded short {i+1}/20")
