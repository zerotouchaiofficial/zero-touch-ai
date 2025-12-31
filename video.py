from moviepy.editor import *

audio = AudioFileClip("voice.wav")

bg = ColorClip(
    size=(1080,1920),
    color=(0,0,0),
    duration=audio.duration
)

txt = TextClip(
    open("fact.txt").read(),
    fontsize=70,
    color="white",
    method="caption",
    size=(1000,None)
).set_position("center").set_duration(audio.duration)

final = CompositeVideoClip([bg, txt]).set_audio(audio)
final.write_videofile("short.mp4", fps=30)
