from moviepy.editor import *
import os
import random

def generate_video(audio_path, facts):
    audio = AudioFileClip(audio_path)

    bg_files = os.listdir("backgrounds")
    bg_path = f"backgrounds/{random.choice(bg_files)}"

    bg = ImageClip(bg_path).set_duration(audio.duration).resize((720,1280))

    duration_per = audio.duration / len(facts)
    text_clips = []

    for i, line in enumerate(facts):
        txt = TextClip(
            line,
            fontsize=60,
            color="white",
            size=(680, 1180),
            method="caption"
        ).set_start(i * duration_per).set_duration(duration_per).set_position("center")
        text_clips.append(txt)

    final = CompositeVideoClip([bg, *text_clips]).set_audio(audio)

    os.makedirs("output", exist_ok=True)
    out = "output/short.mp4"

    final.write_videofile(
        out,
        fps=30,
        codec="libx264",
        audio_codec="aac"
    )

    return out
