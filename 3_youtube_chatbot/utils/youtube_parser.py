import re


class Parser:
    @staticmethod
    def extract_video_id(url: str) -> str:
        pattern = r"(?:v=|youtu\.be/|embed/|shorts/)([a-zA-Z0-9_-]{11})"
        match = re.search(pattern, url)
        if not match:
            raise ValueError("Invalid YouTube URL")
        return match.group(1)
