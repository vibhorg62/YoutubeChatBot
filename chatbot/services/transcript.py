from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled


def get_transcript(video_id):

    try:

        api = YouTubeTranscriptApi()

        transcript = api.fetch(video_id,languages=['en','hi','mr','bn','ta','te','kn','ml','gu','pa'])

        text = " ".join(chunk.text for chunk in transcript)

        return text

    except TranscriptsDisabled:
        raise Exception("Transcript is disabled for this video.")

    except Exception as e:
        raise Exception(str(e))