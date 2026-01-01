import os
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

def get_authenticated_service():
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    return build("youtube", "v3", credentials=creds)

def upload_video():
    if not os.path.exists("videos/short.mp4"):
        raise Exception("Video not found")

    youtube = get_authenticated_service()

    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": "Did you know this? 🤯 #shorts",
                "description": "Mind-blowing fact #shorts",
                "tags": ["shorts", "facts", "didyouknow"],
                "categoryId": "22"
            },
            "status": {
                "privacyStatus": "public",
                "selfDeclaredMadeForKids": False
            }
        },
        media_body=MediaFileUpload(
            "videos/short.mp4",
            chunksize=-1,
            resumable=True
        )
    )

    response = request.execute()
    print("Uploaded:", response["id"])

if __name__ == "__main__":
    upload_video()
