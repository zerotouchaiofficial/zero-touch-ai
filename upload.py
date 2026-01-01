import os, json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

def get_authenticated_service():
    token_json = os.getenv("YOUTUBE_TOKEN_JSON")
    if not token_json:
        raise Exception("YOUTUBE_TOKEN_JSON missing")

    creds_info = json.loads(token_json)
    creds = Credentials.from_authorized_user_info(creds_info, SCOPES)

    return build("youtube", "v3", credentials=creds)

def upload_video():
    youtube = get_authenticated_service()
    print("YouTube authenticated ✔")
