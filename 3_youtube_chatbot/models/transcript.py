from dataclasses import dataclass
from typing import List


@dataclass
class TranscriptSegment:
    text: str
    start: float
    duration: float


@dataclass
class Transcript:
    video_id: str
    text: str
    segments: List[TranscriptSegment]
