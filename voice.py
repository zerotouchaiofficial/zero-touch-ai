import os
import sys

def generate_voice(text):
    os.makedirs("audio", exist_ok=True)
    output_file = "audio/voice.mp3"

    # Free system TTS (works on cloud)
    os.system(f'espeak "{text}" --stdout > {output_file}')
    return output_file


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("No text provided")
    else:
        generate_voice(sys.argv[1])
