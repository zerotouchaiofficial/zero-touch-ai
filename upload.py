import os
import json
import base64
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

def get_authenticated_service():
    token_b64 = os.getenv("YOUTUBE_TOKEN_B64")
    if not token_b64:
        raise Exception("YOUTUBE_TOKEN_B64 secret missing")

    token_json = base64.b64decode(token_b64).decode("utf-8")

    with open("token.json", "w") as f:
        f.write(token_json)

    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    return build("youtube", "v3", credentials=creds)

def upload_video():
    youtube = get_authenticated_service()

    video_path = "videos/final.mp4"

    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": "Mind-Blowing Fact 🤯 #shorts",
                "description": "🔥 AI Fact Short\n\n#facts #shorts #ai #knowledge",
                "tags": ["facts", "shorts", "ai", "knowledge"],
                "categoryId": "27"
            },
            "status": {
                "privacyStatus": "public",
                "selfDeclaredMadeForKids": False
            }
        },
        media_body=MediaFileUpload(video_path, resumable=False)
    )

    response = request.execute()
    print("✅ UPLOADED VIDEO ID:", response["id"])

if __name__ == "__main__":
    upload_video()
