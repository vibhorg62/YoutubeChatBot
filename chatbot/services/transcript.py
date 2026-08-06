import os
import sys
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

    print("STATUS CODE:", response.status_code, file=sys.stderr)
    print("RAW RESPONSE:", response.text, file=sys.stderr)

    if response.status_code != 200:
        raise Exception(response.text)

    data = response.json()

    print("PARSED RESPONSE:", data, file=sys.stderr)

    # ---------------- Case 1 ----------------
    # content = "whole transcript"

    if isinstance(data.get("content"), str):
        return data["content"]

    # ---------------- Case 2 ----------------
    # content = [{text:"..."}, ...]

    if isinstance(data.get("content"), list):

        if len(data["content"]) == 0:
            raise Exception("Transcript is empty.")

        # list of objects
        if isinstance(data["content"][0], dict):

            transcript = " ".join(
                item.get("text", "")
                for item in data["content"]
            )

            return transcript

        # list of strings
        if isinstance(data["content"][0], str):

            return " ".join(data["content"])

    # ---------------- Case 3 ----------------
    # text = "whole transcript"

    if isinstance(data.get("text"), str):
        return data["text"]

    raise Exception(f"Unexpected Supadata response: {data}")