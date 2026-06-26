import re
from typing import Any

from src.core.classifier import Classifier
from src.core.extractor import Extractor
from src.core.summarizer import Summarizer, _split_sentences
from src.core.detector import detect_language


def _count_syllables(word: str) -> int:
    word = word.lower()
    count = 0
    vowels = 'aeiouy'
    if word and word[0] in vowels:
        count += 1
    for i in range(1, len(word)):
        if word[i] in vowels and word[i - 1] not in vowels:
            count += 1
    if word.endswith('e') and count > 1:
        count -= 1
    if word.endswith('le') and len(word) > 2 and word[-3] not in vowels:
        count += 1
    return max(count, 1)


def _readability_score(text: str) -> dict[str, float | str]:
    words = re.findall(r'\w+', text)
    sentences = _split_sentences(text)
    if not sentences or not words:
        return {"score": 0.0, "grade": "N/A"}

    word_count = len(words)
    sentence_count = len(sentences)
    syllable_count = sum(_count_syllables(w) for w in words)

    score = (
        206.835
        - 1.015 * (word_count / sentence_count)
        - 84.6 * (syllable_count / word_count)
    )
    score = max(0.0, min(100.0, score))

    if score >= 90:
        grade = "Very Easy"
    elif score >= 80:
        grade = "Easy"
    elif score >= 70:
        grade = "Fairly Easy"
    elif score >= 60:
        grade = "Standard"
    elif score >= 50:
        grade = "Fairly Difficult"
    elif score >= 30:
        grade = "Difficult"
    else:
        grade = "Very Difficult"

    return {"score": round(score, 2), "grade": grade}


class Analyzer:
    def __init__(self) -> None:
        self._classifier = Classifier()
        self._extractor = Extractor()
        self._summarizer = Summarizer()

    def analyze(self, text: str) -> dict[str, Any]:
        words = re.findall(r'\w+', text)
        sentences = _split_sentences(text)

        word_count = len(words)
        sentence_count = len(sentences)
        char_count = len(text)

        classification = self._classifier.classify(text)
        entities = self._extractor.extract(text)
        summary_result = self._summarizer.summarize(text, ratio=0.3)
        language = detect_language(text)
        readability = _readability_score(text)

        return {
            "word_count": word_count,
            "sentence_count": sentence_count,
            "char_count": char_count,
            "readability": readability,
            "language": language,
            "sentiment": classification["sentiment"],
            "topic": classification["topic"],
            "entities": entities,
            "summary": summary_result["summary"],
        }
