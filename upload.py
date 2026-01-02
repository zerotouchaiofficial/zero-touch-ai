from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import os

youtube = build(
    "youtube", "v3",
    developerKey=os.environ["YOUTUBE_API_KEY"]
)

request = youtube.videos().insert(
    part="snippet,status",
    body={
        "snippet": {
            "title": "Amazing Facts #shorts",
            "description": "Did you know? #shorts #facts",
            "tags": ["shorts", "facts"],
            "categoryId": "22"
        },
        "status": {
            "privacyStatus": "public"
        }
    },
    media_body=MediaFileUpload("videos/short.mp4")
)

request.execute()
print("🚀 Uploaded to YouTube")
