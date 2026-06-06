from services.youtube_transcript_service import YouTubeTranscriptService


def main():
    service = YouTubeTranscriptService()

    url = input("Enter YouTube URL: ")

    transcript = service.get_transcript(url)

    print("\n--- VIDEO ID ---")
    print(transcript.video_id)

    print("\n--- FIRST 500 CHARS ---")
    print(transcript.text)


if __name__ == "__main__":
    main()
