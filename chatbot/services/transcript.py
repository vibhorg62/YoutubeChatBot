from youtube_transcript_api import (
    YouTubeTranscriptApi,
    TranscriptsDisabled,
    NoTranscriptFound
)


def get_transcript(video_id):

    try:

        api = YouTubeTranscriptApi()

        transcript = api.fetch(
            video_id,
            languages=['en', 'hi', 'mr', 'bn', 'ta', 'te', 'kn', 'ml', 'gu', 'pa']
        )

        text = " ".join(
            getattr(chunk, 'text', str(chunk))
            for chunk in transcript
        )

        text = text.encode("utf-8", "replace").decode("utf-8")

        return text

    except TranscriptsDisabled:
        raise Exception("Transcript is disabled for this video.")

    except NoTranscriptFound:
        raise Exception("No transcript found for the requested video.")

    except Exception as e:
        raise Exception(str(e))