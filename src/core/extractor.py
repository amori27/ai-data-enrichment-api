import re

EMAIL_RE = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')
PHONE_RE = re.compile(
    r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
)
DATE_RE = re.compile(
    r'\b\d{4}[-/]\d{1,2}[-/]\d{1,2}\b'
    r'|'
    r'\b\d{1,2}[-/]\d{1,2}[-/]\d{4}\b'
    r'|'
    r'\b(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?'
    r'|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)'
    r'\s+\d{1,2},?\s+\d{4}\b'
)
URL_RE = re.compile(
    r'(?:https?://|www\.)[^\s<>"\'{}|\\^`\[\]]+',
    re.IGNORECASE,
)
HASHTAG_RE = re.compile(r'#\w+')
MENTION_RE = re.compile(r'@\w+')


class Extractor:
    def extract(self, text: str) -> dict[str, list[str]]:
        emails = [m.group(0) for m in EMAIL_RE.finditer(text)]
        phones = [m.group(0).strip() for m in PHONE_RE.finditer(text)]
        dates = [m.group(0).strip() for m in DATE_RE.finditer(text)]
        urls = [m.group(0).rstrip('.,!?;:') for m in URL_RE.finditer(text)]
        hashtags = [m.group(0) for m in HASHTAG_RE.finditer(text)]
        mentions = [m.group(0) for m in MENTION_RE.finditer(text)]

        return {
            "emails": emails,
            "phones": phones,
            "dates": dates,
            "urls": urls,
            "hashtags": hashtags,
            "mentions": mentions,
        }
