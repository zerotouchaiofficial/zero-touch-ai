from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import pickle

with open("youtube_token.pkl", "rb") as f:
    creds = pickle.load(f)

youtube = build("youtube", "v3", credentials=creds)

request = youtube.videos().insert(
    part="snippet,status",
    body={
        "snippet": {
            "title": "Amazing Fact 🤯",
            "description": "Did you know?",
            "tags": ["shorts","facts"],
            "categoryId": "22"
        },
        "status": {
            "privacyStatus": "public"
        }
    },
    media_body=MediaFileUpload("short.mp4")
)

request.execute()
print("🚀 Uploaded")
