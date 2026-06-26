import re
from typing import Any
from collections import Counter


def _split_sentences(text: str) -> list[str]:
    text = text.strip()
    if not text:
        return []
    parts = re.split(r'(?<=[.!?])\s+', text)
    return [p.strip() for p in parts if p.strip()]


def _get_word_freq(text: str) -> Counter:
    words = re.findall(r'\w+', text.lower())
    return Counter(words)


class Summarizer:
    def summarize(
        self,
        text: str,
        ratio: float = 0.3,
        max_sentences: int | None = None,
    ) -> dict[str, Any]:
        sentences = _split_sentences(text)
        if len(sentences) <= 1:
            return {
                "summary": text,
                "original_length": len(text),
                "summary_length": len(text),
                "original_sentences": len(sentences),
                "summary_sentences": len(sentences),
            }

        word_freq = _get_word_freq(text)

        def sentence_score(sentence: str) -> float:
            sent_words = re.findall(r'\w+', sentence.lower())
            if not sent_words:
                return 0.0
            return sum(word_freq.get(w, 0) for w in sent_words) / len(sent_words)

        scored = [(i, sentence_score(s)) for i, s in enumerate(sentences)]
        scored.sort(key=lambda x: x[1], reverse=True)

        num_sentences = max(1, int(len(sentences) * ratio))
        if max_sentences is not None:
            num_sentences = min(num_sentences, max_sentences)

        top_indices = sorted(set(i for i, _ in scored[:num_sentences]))
        summary = ' '.join(sentences[i] for i in top_indices)

        return {
            "summary": summary,
            "original_length": len(text),
            "summary_length": len(summary),
            "original_sentences": len(sentences),
            "summary_sentences": len(top_indices),
        }
