# AI Data Enrichment API

[![Python](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104%2B-009688.svg)](https://fastapi.tiangolo.com)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://docs.astral.sh/ruff/)
[![CI](https://github.com/amori27/ai-data-enrichment-api/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/amori27/ai-data-enrichment-api/actions/workflows/ci-cd.yml)

A lightweight, zero-dependency AI-powered text enrichment API built with FastAPI. Classifies sentiment and topic, extracts entities, generates extractive summaries, detects language, and computes readability scores — all with pure Python, no external ML libraries or API keys required.

## Features

- **Sentiment Analysis** — positive / negative / neutral classification via keyword scoring
- **Topic Detection** — tech, health, business, education, or general categories
- **Entity Extraction** — emails, phone numbers, dates, URLs, hashtags, and mentions via regex
- **Extractive Summarization** — TF-inspired sentence scoring with configurable ratio and sentence count
- **Language Detection** — character-set and common-word matching (en, es, fr, de, zh, ru, ar)
- **Readability Scoring** — Flesch Reading Ease formula with grade labels
- **Full Analysis** — all signals in a single `/analyze` call

## API Reference

| Method | Endpoint       | Description                                  |
|--------|----------------|----------------------------------------------|
| GET    | `/health`      | Health check and version info                |
| POST   | `/classify`    | Sentiment and topic classification           |
| POST   | `/extract`     | Entity extraction (emails, phones, etc.)     |
| POST   | `/summarize`   | Extractive text summarization                |
| POST   | `/analyze`     | All-in-one: classify + extract + summarize   |

### Request / Response Schemas

**POST /classify**
```json
// Request
{"text": "Your text here"}

// Response
{
  "sentiment": "positive",
  "topic": "tech",
  "sentiment_scores": {"positive": 0.85, "negative": 0.0, "neutral": 0.15},
  "topic_scores": {"tech": 0.92, "health": 0.0, "business": 0.08, "education": 0.0, "general": 0.0}
}
```

**POST /extract**
```json
// Request
{"text": "Contact john@example.com or call +1-555-1234"}

// Response
{
  "emails": ["john@example.com"],
  "phones": ["+1-555-1234"],
  "dates": [],
  "urls": [],
  "hashtags": [],
  "mentions": []
}
```

**POST /summarize**
```json
// Request
{"text": "Long text here...", "max_sentences": 3}

// Response
{
  "summary": "Summarized text...",
  "original_length": 500,
  "summary_length": 120,
  "original_sentences": 10,
  "summary_sentences": 3
}
```

**POST /analyze**
```json
// Request
{"text": "Your text here"}

// Response
{
  "word_count": 42,
  "sentence_count": 3,
  "char_count": 210,
  "readability": {"score": 65.4, "grade": "Standard"},
  "language": {"language": "en", "confidence": 0.95},
  "sentiment": "positive",
  "topic": "tech",
  "entities": {"emails": [], "phones": [], "dates": [], "urls": [], "hashtags": [], "mentions": []},
  "summary": "Summarized text..."
}
```

## Quick Start

### Prerequisites

- Python 3.11 or later
- pip

### Installation

```bash
pip install -r requirements.txt
```

### Run the server

```bash
uvicorn src.main:app --reload
```

The API will be available at `http://localhost:8000`.

### Interactive docs

Open `http://localhost:8000/docs` in your browser for the Swagger UI.

## Examples

### Classify text

```bash
curl -X POST http://localhost:8000/classify \
  -H "Content-Type: application/json" \
  -d '{"text":"The new AI model achieves state-of-the-art results"}'
```

### Extract entities

```bash
curl -X POST http://localhost:8000/extract \
  -H "Content-Type: application/json" \
  -d '{"text":"Contact john@example.com or call +1-555-1234"}'
```

### Summarize

```bash
curl -X POST http://localhost:8000/summarize \
  -H "Content-Type: application/json" \
  -d '{"text":"Long text here...", "max_sentences":3}'
```

### Full analysis

```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"text":"Your text here"}'
```

## Development

### Run tests

```bash
python -m pytest tests/ -q
```

### Lint

```bash
ruff check src/ tests/
```

## Project Structure

```
src/
  __init__.py
  main.py              # FastAPI application and route handlers
  core/
    __init__.py
    classifier.py      # Sentiment and topic keyword classification
    extractor.py       # Regex-based entity extraction
    summarizer.py      # TF-inspired extractive summarization
    analyzer.py        # Combined analysis pipeline
    detector.py        # Character-based language detection
  models/
    __init__.py
    schemas.py         # Pydantic request/response models
tests/
  __init__.py
  test_classifier.py
  test_extractor.py
  test_summarizer.py
  test_main.py
```

## License

[MIT](LICENSE)
