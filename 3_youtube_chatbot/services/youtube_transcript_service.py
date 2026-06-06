from youtube_transcript_api import YouTubeTranscriptApi
from models.transcript import Transcript, TranscriptSegment
from utils.youtube_parser import Parser
from youtube_transcript_api.proxies import WebshareProxyConfig
from services.environment_service import EnvironmentService

proxy_details = EnvironmentService().get_proxy_details()


class YouTubeTranscriptService:
    @staticmethod
    def get_transcript(url: str) -> Transcript:
        video_id = Parser.extract_video_id(url)
        raw_transcript = YouTubeTranscriptService._fetch(video_id)
        snippets = raw_transcript.snippets

        segments = [
            TranscriptSegment(
                text=item.text,
                start=item.start,
                duration=item.duration,
            )
            for item in snippets
        ]

        full_text = " ".join(item.text for item in snippets)

        return Transcript(
            video_id=video_id,
            text=full_text,
            segments=segments,
        )

    @staticmethod
    def _fetch(video_id: str):
        try:
            yt = YouTubeTranscriptApi(
                proxy_config=WebshareProxyConfig(
                    proxy_username=proxy_details["user"],
                    proxy_password=proxy_details["pwd"],
                )
            )

            # 👇 BEST OPTION: let library choose best available transcript
            transcript_list = yt.list(video_id)

            # pick "best available" automatically
            transcript = transcript_list.find_generated_transcript(
                transcript_list._manually_created_transcripts.keys()
            ) if transcript_list._manually_created_transcripts else transcript_list.find_generated_transcript(
                transcript_list._generated_transcripts.keys()
            )

            return transcript.fetch()

        except Exception as e:
            raise RuntimeError(f"Failed to fetch transcript: {str(e)}")
