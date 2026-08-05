from urllib.parse import urlparse, parse_qs

def extract_video_id(url):

    parsed = urlparse(url)

    if parsed.hostname in ["www.youtube.com", "youtube.com"]:
        return parse_qs(parsed.query).get("v", [None])[0]

    elif parsed.hostname == "youtu.be":
        return parsed.path[1:]

    return None