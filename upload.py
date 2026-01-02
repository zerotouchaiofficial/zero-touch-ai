from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials
import json
import os

def upload_video(video_path, topic):
    creds = Credentials.from_authorized_user_info(
        json.loads(os.environ["YT_TOKEN"]),
        ["https://www.googleapis.com/auth/youtube.upload"]
    )

    youtube = build("youtube", "v3", credentials=creds)

    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": f"{topic} Facts You Didn’t Know #shorts",
                "description": f"60 seconds of mind-blowing facts about {topic}.",
                "tags": [topic, "facts", "shorts", "viral"],
                "categoryId": "27"
            },
            "status": {
                "privacyStatus": "public"
            }
        },
        media_body=MediaFileUpload(video_path, resumable=True)
    )

    request.execute()
