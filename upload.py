from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import pickle
import os

VIDEO_PATH = "videos/short.mp4"
TOKEN_FILE = "youtube_token.pkl"

# load oauth token
with open(TOKEN_FILE, "rb") as f:
    creds = pickle.load(f)

youtube = build("youtube", "v3", credentials=creds)

request = youtube.videos().insert(
    part="snippet,status",
    body={
        "snippet": {
            "title": "Amazing Facts #shorts",
            "description": "Did you know? #shorts",
            "tags": ["shorts", "facts"],
            "categoryId": "22"
        },
        "status": {
            "privacyStatus": "public"
        }
    },
    media_body=MediaFileUpload(
        VIDEO_PATH,
        mimetype="video/mp4",
        resumable=True
    )
)

response = request.execute()
print("🚀 Uploaded video ID:", response["id"])
