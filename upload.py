import pickle
import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

TOKEN_FILE = "youtube_token.pkl"

if not os.path.exists(TOKEN_FILE) or os.path.getsize(TOKEN_FILE) == 0:
    raise RuntimeError("❌ YouTube token missing or empty")

with open(TOKEN_FILE, "rb") as f:
    creds = pickle.load(f)

youtube = build("youtube", "v3", credentials=creds)

request = youtube.videos().insert(
    part="snippet,status",
    body={
        "snippet": {
            "title": "Amazing Fact 🤯 #shorts",
            "description": "Did you know?",
            "tags": ["shorts", "facts", "viral"],
            "categoryId": "22"
        },
        "status": {
            "privacyStatus": "public"
        }
    },
    media_body=MediaFileUpload("short.mp4", chunksize=-1, resumable=True)
)

request.execute()
print("🚀 Upload successful")
