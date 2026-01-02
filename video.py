from moviepy.editor import *
import random, os

def make_video(audio_path, facts):
    audio = AudioFileClip(audio_path)
    bg = ImageClip("backgrounds/bg1.png").set_duration(audio.duration)

    duration = audio.duration / len(facts)
    texts = []

    for i, line in enumerate(facts):
        txt = TextClip(
            line,
            fontsize=60,
            color="white",
            size=(720,1280),
            method="caption"
        ).set_start(i*duration).set_duration(duration).set_position("center")
        texts.append(txt)

    final = CompositeVideoClip([bg, *texts]).set_audio(audio)
    out = "output/short.mp4"
    final.write_videofile(out, fps=30)

    return out
