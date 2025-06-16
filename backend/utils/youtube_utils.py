# youtube-analyzer-backend/utils/youtube_utils.py

def extract_video_id(url: str) -> str:
    import re
    match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", url)
    if match:
        return match.group(1)
    else:
        raise ValueError("Invalid YouTube URL")
