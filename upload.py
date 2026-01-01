import os
import pickle
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

VIDEO_PATH = "videos/short.mp4"

def get_authenticated_service():
    if not os.path.exists("token.json"):
        raise Exception("token.json missing. Generate it locally first.")

    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    return build("youtube", "v3", credentials=creds)

def upload_video():
    # HARD FAIL CHECKS (VERY IMPORTANT)
    if not os.path.exists(VIDEO_PATH):
        raise Exception("short.mp4 not found")

    size = os.path.getsize(VIDEO_PATH)
    if size < 1_000_000:
        raise Exception("Video too small, YouTube will abandon processing")

    youtube = get_authenticated_service()

    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": "Mind Blowing Fact 🤯 #shorts",
                "description": "Amazing fact you didn't know!",
                "tags": ["shorts", "facts", "mindblowing"],
                "categoryId": "27"
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

    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"Upload progress: {int(status.progress() * 100)}%")

    print("UPLOAD SUCCESSFUL")
    print("VIDEO ID:", response["id"])

if __name__ == "__main__":
    upload_video()
