from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials
import os, json

def upload_video(path, topic):
    creds = Credentials.from_authorized_user_info(
        json.loads(os.environ["YT_TOKEN"]),
        ["https://www.googleapis.com/auth/youtube.upload"]
    )

    yt = build("youtube", "v3", credentials=creds)

    request = yt.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": f"{topic} Facts You Didn’t Know #shorts",
                "description": f"60 seconds of amazing {topic} facts.",
                "tags": [topic, "facts", "shorts"]
            },
            "status": {"privacyStatus": "public"}
        },
        media_body=MediaFileUpload(path)
    )

    request.execute()
