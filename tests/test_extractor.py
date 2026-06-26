from src.core.extractor import Extractor


def test_extract_email():
    extractor = Extractor()
    result = extractor.extract("Contact me at john.doe@example.com for details.")
    assert "john.doe@example.com" in result["emails"]


def test_extract_multiple_emails():
    extractor = Extractor()
    result = extractor.extract("Email a@b.com or c@d.com.")
    assert len(result["emails"]) == 2


def test_extract_phone():
    extractor = Extractor()
    result = extractor.extract("Call +1-555-123-4567 for support.")
    assert len(result["phones"]) >= 1


def test_extract_url():
    extractor = Extractor()
    result = extractor.extract("Visit https://example.com/page for more info.")
    assert len(result["urls"]) >= 1


def test_extract_hashtag():
    extractor = Extractor()
    result = extractor.extract("This is trending #AI and #Tech.")
    assert "#AI" in result["hashtags"]
    assert "#Tech" in result["hashtags"]


def test_extract_mention():
    extractor = Extractor()
    result = extractor.extract("Follow @username and @company for updates.")
    assert "@username" in result["mentions"]
    assert "@company" in result["mentions"]


def test_extract_date():
    extractor = Extractor()
    result = extractor.extract("The event is on January 15, 2024.")
    assert len(result["dates"]) >= 1


def test_no_entities():
    extractor = Extractor()
    result = extractor.extract("This is plain text with no entities.")
    assert all(len(v) == 0 for v in result.values())
