from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

def get_authenticated_service():
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    return build("youtube", "v3", credentials=creds)

def upload_video():
    youtube = get_authenticated_service()

    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": "🤯 Mind-Blowing AI Fact #Shorts",
                "description": (
                    "Did you know this?\n\n"
                    "🔥 Daily AI Facts\n"
                    "⚡ Zero Touch AI\n\n"
                    "#shorts #facts #aifacts #knowledge #ytshorts"
                ),
                "categoryId": "27"
            },
            "status": {
                "privacyStatus": "public",
                "selfDeclaredMadeForKids": False
            }
        },
        media_body=MediaFileUpload(VIDEO_FILE, resumable=True)
    )

    response = request.execute()
    print("UPLOADED VIDEO ID:", response["id"])


if __name__ == "__main__":
    upload_video()
