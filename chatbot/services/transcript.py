import os
import requests


SUPADATA_URL = "https://api.supadata.ai/v1/transcript"


def get_transcript(video_url):

    api_key = os.getenv("SUPADATA_API_KEY")

    if not api_key:
        raise Exception("SUPADATA_API_KEY not found.")

    headers = {
        "x-api-key": api_key
    }

    params = {
        "url": video_url,
        "text": "true"
    }

    response = requests.get(
        SUPADATA_URL,
        headers=headers,
        params=params,
        timeout=60
    )

    if response.status_code != 200:
        raise Exception(response.text)

    data = response.json()

    if "content" not in data:
        raise Exception("Transcript not found.")

    transcript = " ".join(
        chunk["text"]
        for chunk in data["content"]
    )

    return transcript.encode(
        "utf-8",
        "replace"
    ).decode("utf-8")