import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
VIDEO_PATH = "videos/short.mp4"

def get_authenticated_service():
    if not os.path.exists("token.json"):
        raise Exception("token.json missing — upload cannot continue")

    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    return build("youtube", "v3", credentials=creds)

def upload_video():
    if not os.path.exists(VIDEO_PATH):
        raise Exception("Video not found: " + VIDEO_PATH)

    youtube = get_authenticated_service()

    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": "Did you know this? 🤯 #shorts",
                "description": "Auto uploaded by Zero Touch AI",
                "tags": ["shorts", "facts", "ai"],
                "categoryId": "22"
            },
            "status": {
                "privacyStatus": "public",
                "selfDeclaredMadeForKids": False
            }
        },
        media_body=MediaFileUpload(
            VIDEO_PATH,
            mimetype="video/mp4",
            resumable=True
        )
    )

    response = request.execute()
    print("Uploaded video ID:", response["id"])

if __name__ == "__main__":
    upload_video()
