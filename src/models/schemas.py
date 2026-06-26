from pydantic import BaseModel, Field
from typing import Optional


class ClassifyRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Text to classify")


class ClassifyResponse(BaseModel):
    sentiment: str
    topic: str
    sentiment_scores: dict[str, float]
    topic_scores: dict[str, float]


class ExtractRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Text to extract entities from")


class ExtractResponse(BaseModel):
    emails: list[str]
    phones: list[str]
    dates: list[str]
    urls: list[str]
    hashtags: list[str]
    mentions: list[str]


class SummarizeRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Text to summarize")
    ratio: Optional[float] = Field(None, ge=0.1, le=1.0, description="Summary ratio (0.1-1.0)")
    max_sentences: Optional[int] = Field(None, ge=1, le=100, description="Maximum number of sentences")


class SummarizeResponse(BaseModel):
    summary: str
    original_length: int
    summary_length: int
    original_sentences: int
    summary_sentences: int


class AnalyzeRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Text to analyze")


class AnalyzeResponse(BaseModel):
    word_count: int
    sentence_count: int
    char_count: int
    readability: dict[str, float | str]
    language: dict[str, str | float]
    sentiment: str
    topic: str
    entities: dict[str, list[str]]
    summary: str
