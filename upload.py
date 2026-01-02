from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import pickle

VIDEO_PATH = "videos/short.mp4"
TOKEN_FILE = "youtube_token.pkl"

with open(TOKEN_FILE, "rb") as f:
    creds = pickle.load(f)

youtube = build("youtube", "v3", credentials=creds)

request = youtube.videos().insert(
    part="snippet,status",
    body={
        "snippet": {
            "title": "Amazing Fact #shorts",
            "description": "Auto uploaded via CI 🚀",
            "tags": ["shorts", "facts", "ai"],
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
