import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

def upload_video():
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    youtube = build("youtube", "v3", credentials=creds)

    video_file = "videos/short.mp4"

    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": "Did You Know? 🤯",
                "description": "#shorts #facts",
                "tags": ["shorts", "facts"],
                "categoryId": "27"
            },
            "status": {
                "privacyStatus": "public"
            }
        },
        media_body=MediaFileUpload(video_file, resumable=True)
    )

    response = request.execute()
    print("Uploaded video ID:", response["id"])

if __name__ == "__main__":
    upload_video()
