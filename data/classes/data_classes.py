from dataclasses import dataclass
from typing import Optional

@dataclass
class ScrapeResult:
    topic: str
    subtopic: str
    data: list[dict]


@dataclass
class NewsArticle:
    headline: str
    description: str
    url: Optional[str] = None
    sentiment_label: Optional[str] = None
    sentiment_score: Optional[float] = None


