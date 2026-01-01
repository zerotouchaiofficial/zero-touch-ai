import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

def get_authenticated_service():
    if not os.path.exists("token.json"):
        raise Exception("token.json missing")

    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    return build("youtube", "v3", credentials=creds)

def upload_video():
    video_file = "videos/short.mp4"

    if not os.path.exists(video_file):
        raise Exception("Video file not found")

    size_kb = os.path.getsize(video_file) / 1024
    if size_kb < 300:
        raise Exception("Video too small (<300KB)")

    youtube = get_authenticated_service()

    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": "Mind Blowing AI Fact 🤯 #shorts",
                "description": "AI generated facts\n#shorts #facts #ai",
                "tags": ["ai", "facts", "shorts"],
                "categoryId": "27"
            },
            "status": {
                "privacyStatus": "public",
                "selfDeclaredMadeForKids": False
            }
        },
        media_body=MediaFileUpload(video_file, resumable=True)
    )

    response = request.execute()
    print("Uploaded Video ID:", response["id"])

if __name__ == "__main__":
    upload_video()
