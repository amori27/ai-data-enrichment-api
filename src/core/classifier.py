from typing import Any

POSITIVE_KEYWORDS = frozenset({
    "amazing", "awesome", "beautiful", "best", "better", "brilliant",
    "creative", "delightful", "excellent", "exceptional", "fantastic",
    "fine", "good", "grand", "great", "happy", "impressive", "incredible",
    "innovative", "inspired", "lovely", "magnificent", "nice",
    "outstanding", "perfect", "phenomenal", "pleasant", "pleased",
    "positive", "remarkable", "splendid", "stunning", "superb",
    "terrific", "wonderful", "worthwhile", "success", "successful",
    "breakthrough", "groundbreaking", "fascinating", "thrilled",
    "excited", "delighted", "grateful", "hopeful", "optimistic",
})

NEGATIVE_KEYWORDS = frozenset({
    "abysmal", "adverse", "angry", "annoying", "awful", "bad",
    "broken", "confusing", "corrupt", "damage", "damaged",
    "dangerous", "defective", "deficient", "depressing",
    "destructive", "difficult", "disastrous", "dreadful",
    "error", "failed", "failure", "faulty", "flawed",
    "frustrating", "garbage", "glitch", "grave", "grim",
    "gross", "horrible", "horrific", "hurtful", "inadequate",
    "inferior", "irritating", "lousy", "miserable", "nasty",
    "negative", "nightmare", "nuisance", "offensive", "painful",
    "pathetic", "poor", "problem", "problematic", "regret",
    "regretful", "sad", "severe", "shame", "shocking", "sick",
    "sorry", "substandard", "suffer", "terrible", "tragic",
    "ugly", "unable", "unfortunate", "unhappy", "unsatisfactory",
    "useless", "violent", "wasteful", "weak", "worse", "worst",
    "wrong", "crisis", "disaster", "catastrophic", "critical",
})

TOPIC_KEYWORDS: dict[str, frozenset[str]] = {
    "tech": frozenset({
        "technology", "tech", "digital", "software", "hardware",
        "computer", "computing", "data", "ai", "artificial intelligence",
        "machine learning", "deep learning", "algorithm", "code",
        "coding", "developer", "programming", "app", "application",
        "startup", "innovation", "cyber", "security", "blockchain",
        "crypto", "cryptocurrency", "internet", "web", "online",
        "platform", "system", "network", "server", "cloud",
        "database", "api", "framework", "engineer", "engineering",
        "robot", "robotic", "automation", "autonomous", "electric",
        "electronic", "device", "gadget", "smartphone", "mobile",
        "sass", "open source", "repository", "deploy", "devops",
        "container", "microservice", "frontend", "backend", "fullstack",
    }),
    "health": frozenset({
        "health", "healthcare", "medical", "medicine", "doctor",
        "hospital", "patient", "treatment", "therapy", "diagnosis",
        "disease", "drug", "medication", "pharmacy", "clinical",
        "surgery", "surgical", "wellness", "fitness", "nutrition",
        "diet", "exercise", "mental health", "vaccine", "vaccination",
        "immune", "immunity", "epidemic", "pandemic", "covid",
        "coronavirus", "symptom", "prevention", "cure", "nurse",
        "physician", "specialist", "dental", "optical", "hearing",
        "therapeutic", "diagnostic", "screening", "symptom",
        "chronic", "acute", "rehabilitation", "pharmaceutical",
    }),
    "business": frozenset({
        "business", "company", "corporation", "enterprise",
        "entrepreneur", "entrepreneurship", "market", "marketing",
        "sales", "revenue", "profit", "loss", "investment",
        "investor", "funding", "venture", "capital", "finance",
        "financial", "bank", "banking", "economy", "economic",
        "trade", "commerce", "commercial", "industry", "industrial",
        "management", "manager", "leadership", "strategy",
        "strategic", "growth", "expansion", "merger", "acquisition",
        "ipo", "stock", "bond", "dividend", "shareholder",
        "stakeholder", "ceo", "cfo", "cto", "board", "director",
        "executive", "consulting", "consultant", "firm", "partnership",
        "startup", "scaleup", "unicorn", "valuation", "audit",
        "compliance", "regulatory", "fiscal", "monetary",
    }),
    "education": frozenset({
        "education", "school", "university", "college", "student",
        "teacher", "professor", "instructor", "educator", "learning",
        "teaching", "course", "curriculum", "degree", "diploma",
        "certificate", "certification", "training", "workshop",
        "seminar", "lecture", "class", "classroom", "academic",
        "research", "study", "studies", "scholarship", "tuition",
        "enrollment", "admission", "graduate", "undergraduate",
        "phd", "master", "bachelor", "exam", "test", "assessment",
        "grade", "score", "homework", "assignment", "project",
        "thesis", "dissertation", "library", "textbook", "knowledge",
        "skill", "k-12", "primary", "secondary", "elementary",
        "faculty", "dean", "curriculum", "syllabus", "pedagogy",
    }),
    "general": frozenset(),
}


class Classifier:
    def classify(self, text: str) -> dict[str, Any]:
        text_lower = text.lower()

        sentiment_scores: dict[str, float] = {}
        for sentiment, keywords in [("positive", POSITIVE_KEYWORDS), ("negative", NEGATIVE_KEYWORDS)]:
            count = sum(1 for kw in keywords if kw in text_lower)
            sentiment_scores[sentiment] = float(count)

        if all(v == 0.0 for v in sentiment_scores.values()):
            sentiment_scores = {"positive": 0.0, "negative": 0.0, "neutral": 1.0}
            best_sentiment = "neutral"
        else:
            sentiment_scores.setdefault("neutral", 0.0)
            best_sentiment = max(sentiment_scores, key=sentiment_scores.get)

        total_sent = sum(sentiment_scores.values())
        sentiment_probs = {
            k: round(v / total_sent, 4) for k, v in sentiment_scores.items()
        } if total_sent > 0 else {"neutral": 1.0}

        topic_scores: dict[str, float] = {}
        for topic, keywords in TOPIC_KEYWORDS.items():
            count = sum(1 for kw in keywords if kw in text_lower)
            topic_scores[topic] = float(count)

        if all(v == 0.0 for v in topic_scores.values()):
            topic_scores["general"] = 1.0

        total_topic = sum(topic_scores.values())
        topic_probs = {
            k: round(v / total_topic, 4) for k, v in topic_scores.items()
        } if total_topic > 0 else {"general": 1.0}

        best_topic = max(topic_scores, key=topic_scores.get)

        return {
            "sentiment": best_sentiment,
            "topic": best_topic,
            "sentiment_scores": sentiment_probs,
            "topic_scores": topic_probs,
        }
