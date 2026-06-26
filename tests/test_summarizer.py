from src.core.summarizer import Summarizer


def test_summarize_short_text():
    summarizer = Summarizer()
    result = summarizer.summarize("Short text.")
    assert result["summary"] == "Short text."


def test_summarize_longer_text():
    summarizer = Summarizer()
    text = (
        "Artificial intelligence is transforming the modern world. "
        "Machine learning algorithms can process vast amounts of data. "
        "Deep neural networks have achieved remarkable results in image recognition. "
        "Natural language processing enables computers to understand human language. "
        "These technologies are being deployed across many industries."
    )
    result = summarizer.summarize(text, ratio=0.5)
    assert len(result["summary"]) < len(text)
    assert result["original_sentences"] == 5
    assert result["summary_sentences"] <= 3


def test_summarize_with_max_sentences():
    summarizer = Summarizer()
    text = (
        "First sentence about technology. "
        "Second sentence about science. "
        "Third sentence about engineering. "
        "Fourth sentence about mathematics. "
        "Fifth sentence about philosophy."
    )
    result = summarizer.summarize(text, max_sentences=2)
    assert result["summary_sentences"] <= 2


def test_summarize_preserves_original_order():
    summarizer = Summarizer()
    text = (
        "First sentence about artificial intelligence. "
        "Second sentence about machine learning. "
        "Third sentence about deep learning. "
        "Fourth sentence about neural networks. "
        "Fifth sentence about data science."
    )
    result = summarizer.summarize(text, ratio=0.8)
    indices = [result["summary"].find(s) for s in text.split(". ") if s[:10] in result["summary"]]
    assert indices == sorted(indices)
