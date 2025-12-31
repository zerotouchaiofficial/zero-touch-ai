from moviepy.editor import ColorClip, AudioFileClip

def create_video(audio_path, output_path):
    audio = AudioFileClip(audio_path)

    video = ColorClip(
        size=(1080, 1920),
        color=(0, 0, 0),
        duration=audio.duration
    )

    video = video.set_audio(audio)
    video.write_videofile(
        output_path,
        fps=30,
        codec="libx264",
        audio_codec="aac"
    )
