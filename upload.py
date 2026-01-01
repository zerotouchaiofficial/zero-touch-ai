import os, time, random
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

def get_service():
    flow = InstalledAppFlow.from_client_secrets_file(
        "credentials.json", SCOPES
    )
    creds = flow.run_console()
    return build("youtube", "v3", credentials=creds)

youtube = get_service()

title_variants = [
    "Did you know this?",
    "Most people don’t know this",
    "Random fact",
    "Mind blowing fact",
    "Crazy but true"
]

with open("current_fact.txt") as f:
    fact = f.read()

request = youtube.videos().insert(
    part="snippet,status",
    body={
        "snippet": {
            "title": random.choice(title_variants),
            "description": fact,
            "tags": ["shorts", "facts"],
            "categoryId": "22"
        },
        "status": {
            "privacyStatus": "public"
        }
    },
    media_body=MediaFileUpload(
        "videos/short.mp4",
        resumable=True
    )
)

request.execute()
print("Uploaded")
