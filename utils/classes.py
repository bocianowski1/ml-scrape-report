from dataclasses import dataclass
from typing import Optional


@dataclass
class NewsArticle:
    headline: str
    description: str
    url: str
    sentiment_label: Optional[str] = None
    sentiment_score: Optional[float] = None


