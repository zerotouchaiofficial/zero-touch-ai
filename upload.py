import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

VIDEO_FILE = "videos/output.mp4"

def get_authenticated_service():
    if not os.path.exists("token.json"):
        raise Exception("token.json missing — upload stopped")

    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    return build("youtube", "v3", credentials=creds)

def upload_video():
    if not os.path.exists(VIDEO_FILE):
        raise Exception("Video file not found")

    youtube = get_authenticated_service()

    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": "AI Fact You Didn’t Know 🤯 #shorts",
                "description": "AI Generated Facts • Zero Touch AI",
                "tags": ["ai", "facts", "shorts"],
                "categoryId": "28"
            },
            "status": {
                "privacyStatus": "public",
                "selfDeclaredMadeForKids": False
            }
        },
        media_body=MediaFileUpload(VIDEO_FILE, resumable=True)
    )

    response = request.execute()
    print("Uploaded Video ID:", response["id"])

if __name__ == "__main__":
    upload_video()
