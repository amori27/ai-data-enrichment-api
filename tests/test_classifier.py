from src.core.classifier import Classifier


def test_positive_sentiment():
    classifier = Classifier()
    result = classifier.classify("This product is absolutely amazing and wonderful!")
    assert result["sentiment"] == "positive"
    assert result["sentiment_scores"]["positive"] > 0


def test_negative_sentiment():
    classifier = Classifier()
    result = classifier.classify("This is a terrible and awful experience. Very disappointing.")
    assert result["sentiment"] == "negative"
    assert result["sentiment_scores"]["negative"] > 0


def test_neutral_sentiment():
    classifier = Classifier()
    result = classifier.classify("The meeting is scheduled for tomorrow at 3pm.")
    assert result["sentiment"] == "neutral"


def test_topic_tech():
    classifier = Classifier()
    result = classifier.classify("The new AI algorithm improves machine learning model accuracy.")
    assert result["topic"] == "tech"


def test_topic_health():
    classifier = Classifier()
    result = classifier.classify("The patient responded well to the new treatment and therapy.")
    assert result["topic"] == "health"


def test_topic_business():
    classifier = Classifier()
    result = classifier.classify("The company reported strong revenue growth this quarter.")
    assert result["topic"] == "business"


def test_topic_education():
    classifier = Classifier()
    result = classifier.classify("Students at the university are learning from an updated curriculum.")
    assert result["topic"] == "education"


def test_topic_general():
    classifier = Classifier()
    result = classifier.classify("The weather is nice today.")
    assert result["topic"] == "general"


def test_scores_are_probabilities():
    classifier = Classifier()
    result = classifier.classify("I love this new technology!")
    total = sum(result["sentiment_scores"].values())
    assert abs(total - 1.0) < 0.01
    total = sum(result["topic_scores"].values())
    assert abs(total - 1.0) < 0.01
