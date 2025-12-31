from moviepy import ColorClip, AudioFileClip
import os

def create_short(audio_file, output_file):
    # Ensure output folder exists
    os.makedirs("videos", exist_ok=True)

    # Load audio
    audio = AudioFileClip(audio_file)

    # Create vertical (Shorts) video
    clip = ColorClip(
        size=(1080, 1920),
        color=(0, 0, 0),
        duration=audio.duration
    )

    clip = clip.set_audio(audio)

    # Export video
    clip.write_videofile(
        output_file,
        fps=24,
        codec="libx264",
        audio_codec="aac"
    )


if __name__ == "__main__":
    create_short("audio/voice.mp3", "videos/short.mp4")
