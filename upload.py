import os
import base64
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

VIDEO_PATH = "videos/output.mp4"   # change ONLY if your video name is different
TITLE = "AI Fact 🤯"
DESCRIPTION = "Subscribe for more AI facts"
TAGS = ["ai", "facts", "shorts"]
CATEGORY_ID = "22"  # People & Blogs
PRIVACY_STATUS = "public"


def get_authenticated_service():
    # 🔥 THIS IS THE KEY PART
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

    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": TITLE,
                "description": DESCRIPTION,
                "tags": TAGS,
                "categoryId": CATEGORY_ID,
            },
            "status": {
                "privacyStatus": PRIVACY_STATUS,
                "selfDeclaredMadeForKids": False,
            },
        },
        media_body=MediaFileUpload(VIDEO_PATH, resumable=True),
    )

    response = request.execute()
    print("✅ UPLOADED VIDEO ID:", response["id"])


if __name__ == "__main__":
    upload_video()
