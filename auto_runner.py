import subprocess
import sys

print("▶ Starting video generation...")
subprocess.run([sys.executable, "generate_video.py"], check=True)

print("▶ Starting upload step...")
subprocess.run([sys.executable, "upload.py"], check=True)

print("✅ Pipeline finished")
