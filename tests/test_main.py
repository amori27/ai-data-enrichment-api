import pytest
from fastapi.testclient import TestClient

from src.main import app


@pytest.fixture
def client():
    return TestClient(app)


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["version"] == "1.0.0"


def test_classify(client):
    response = client.post("/classify", json={"text": "This product is absolutely amazing!"})
    assert response.status_code == 200
    data = response.json()
    assert data["sentiment"] == "positive"


def test_extract(client):
    response = client.post("/extract", json={"text": "Email test@example.com"})
    assert response.status_code == 200
    data = response.json()
    assert "test@example.com" in data["emails"]


def test_summarize(client):
    text = (
        "First sentence about AI technology. "
        "Second sentence about machine learning. "
        "Third sentence about deep neural networks. "
        "Fourth sentence about natural language processing."
    )
    response = client.post("/summarize", json={"text": text, "max_sentences": 2})
    assert response.status_code == 200
    data = response.json()
    assert data["summary_sentences"] <= 2


def test_analyze(client):
    text = "Artificial intelligence is revolutionizing healthcare. New diagnostic tools are being developed."
    response = client.post("/analyze", json={"text": text})
    assert response.status_code == 200
    data = response.json()
    assert data["word_count"] > 0
    assert data["sentence_count"] > 0
    assert "sentiment" in data
    assert "topic" in data
    assert "entities" in data
    assert "summary" in data
    assert "readability" in data
    assert "language" in data


def test_empty_text_returns_422(client):
    response = client.post("/classify", json={"text": ""})
    assert response.status_code == 422


def test_summarize_default_ratio(client):
    text = (
        "First sentence about artificial intelligence. "
        "Second sentence about machine learning. "
        "Third sentence about deep learning. "
        "Fourth sentence about neural networks. "
        "Fifth sentence about data science. "
        "Sixth sentence about computer vision. "
        "Seventh sentence about reinforcement learning. "
        "Eighth sentence about robotics. "
        "Ninth sentence about automation. "
        "Tenth sentence about intelligent systems."
    )
    response = client.post("/summarize", json={"text": text})
    assert response.status_code == 200
    data = response.json()
    assert data["summary_sentences"] <= 3
