import os, json
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.http import MediaFileUpload

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

# recreate credentials.json from secret
with open("credentials.json", "w") as f:
    f.write(os.getenv("GOOGLE_CREDENTIALS_JSON"))

flow = InstalledAppFlow.from_client_secrets_file(
    "credentials.json", SCOPES
)
credentials = flow.run_console()

youtube = build("youtube", "v3", credentials=credentials)

request = youtube.videos().insert(
    part="snippet,status",
    body={
        "snippet": {
            "title": "This Fact Will Blow Your Mind 🤯 #shorts",
            "description": open("fact.txt").read()
            + "\n\n#zerotouchai #facts #shorts #science #ai",
            "categoryId": "27"
        },
        "status": {
            "privacyStatus": "public"
        }
    },
    media_body=MediaFileUpload("short.mp4")
)

request.execute()
