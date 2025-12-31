import os
import pickle
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

VIDEO_FILE = "videos/short.mp4"
FACT_FILE = "fact.txt"


def get_authenticated_service():
    creds = None

    if os.path.exists("token.json"):
        with open("token.json", "rb") as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open("token.json", "wb") as token:
            pickle.dump(creds, token)

    return build("youtube", "v3", credentials=creds)


def read_fact():
    if os.path.exists(FACT_FILE):
        with open(FACT_FILE, "r") as f:
            return f.read().strip()
    return "Mind-Blowing AI Fact"


def build_metadata(fact):
    title = f"🤯 {fact[:60]} #Shorts"

    description = (
        f"{fact}\n\n"
        "⚡ Daily AI Facts\n"
        "🧠 Smart, Short & Addictive\n\n"
        "#shorts #aifacts #facts #ytshorts #knowledge"
    )

    tags = [
        "AI facts",
        "facts",
        "shorts",
        "did you know",
        "knowledge",
        "viral shorts",
        "mind blowing facts"
    ]

    return title, description, tags


def upload_video():
    youtube = get_authenticated_service()

    fact = read_fact()
    title, description, tags = build_metadata(fact)

    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": title,
                "description": description,
                "tags": tags,
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
