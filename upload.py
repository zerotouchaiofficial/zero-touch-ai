import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

def get_authenticated_service():
    if not os.path.exists("token.json"):
        raise Exception("token.json missing")

    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    return build("youtube", "v3", credentials=creds)

def upload_video():
    video_path = "videos/short.mp4"

    if not os.path.exists(video_path):
        raise Exception("Video not found")

    size_mb = os.path.getsize(video_path) / (1024 * 1024)
    if size_mb < 1:
        raise Exception("Video too small (<1MB) — YouTube will abandon")

    youtube = get_authenticated_service()

    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": "Mind-Blowing Fact 🤯",
                "description": "#shorts",
                "tags": ["shorts"],
                "categoryId": "22"
            },
            "status": {
                "privacyStatus": "public"
            }
        },
        media_body=MediaFileUpload(video_path, resumable=True)
    )

    response = request.execute()
    print("UPLOADED:", response["id"])

if __name__ == "__main__":
    upload_video()
