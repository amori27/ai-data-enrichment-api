from fastapi import FastAPI

from src.models.schemas import (
    ClassifyRequest,
    ClassifyResponse,
    ExtractRequest,
    ExtractResponse,
    SummarizeRequest,
    SummarizeResponse,
    AnalyzeRequest,
    AnalyzeResponse,
)
from src.core.classifier import Classifier
from src.core.extractor import Extractor
from src.core.summarizer import Summarizer
from src.core.analyzer import Analyzer

app = FastAPI(title="AI Data Enrichment API", version="1.0.0")

classifier = Classifier()
extractor = Extractor()
summarizer = Summarizer()
analyzer = Analyzer()


@app.get("/health")
def health():
    return {"status": "ok", "version": "1.0.0"}


@app.post("/classify", response_model=ClassifyResponse)
def classify_endpoint(request: ClassifyRequest):
    result = classifier.classify(request.text)
    return ClassifyResponse(**result)


@app.post("/extract", response_model=ExtractResponse)
def extract_endpoint(request: ExtractRequest):
    result = extractor.extract(request.text)
    return ExtractResponse(**result)


@app.post("/summarize", response_model=SummarizeResponse)
def summarize_endpoint(request: SummarizeRequest):
    result = summarizer.summarize(
        request.text,
        ratio=request.ratio or 0.3,
        max_sentences=request.max_sentences,
    )
    return SummarizeResponse(**result)


@app.post("/analyze", response_model=AnalyzeResponse)
def analyze_endpoint(request: AnalyzeRequest):
    result = analyzer.analyze(request.text)
    return AnalyzeResponse(**result)
