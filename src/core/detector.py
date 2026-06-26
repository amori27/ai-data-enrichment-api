from typing import Any

_EN_WORDS = frozenset({
    'the', 'is', 'are', 'was', 'were', 'have', 'has', 'been', 'will',
    'would', 'could', 'should', 'this', 'that', 'these', 'those',
    'and', 'but', 'for', 'nor', 'yet', 'with', 'from', 'they', 'them',
    'their', 'what', 'when', 'where', 'which', 'who', 'how', 'all',
    'each', 'every', 'some', 'any', 'no', 'not', 'only', 'very',
    'just', 'also', 'more', 'most', 'much', 'many', 'such', 'than',
    'then', 'now', 'here', 'there', 'about', 'into', 'over', 'after',
    'before', 'between', 'through', 'during', 'because', 'since',
    'while', 'although', 'though', 'if', 'as', 'so', 'than', 'or',
})

_ES_WORDS = frozenset({
    'el', 'la', 'los', 'las', 'un', 'una', 'y', 'e', 'o', 'u',
    'pero', 'sino', 'que', 'de', 'del', 'al', 'por', 'para', 'con',
    'sin', 'sobre', 'entre', 'es', 'son', 'estoy', 'estas', 'esta',
    'estamos', 'estais', 'estan', 'he', 'has', 'ha', 'hemos', 'han',
    'ser', 'haber', 'tener', 'hacer', 'poder', 'decir', 'ir', 'ver',
    'dar', 'saber', 'querer', 'venir', 'yo', 'tu', 'el', 'ella',
    'usted', 'nosotros', 'vosotros', 'ellos', 'ellas', 'ustedes',
    'mi', 'me', 'lo', 'le', 'la', 'se', 'te', 'nos', 'os',
})

_FR_WORDS = frozenset({
    'le', 'la', 'les', 'un', 'une', 'des', 'du', 'de', 'et', 'ou',
    'mais', 'donc', 'car', 'ni', 'or', 'que', 'qui', 'dans', 'sur',
    'avec', 'pour', 'par', 'est', 'sont', 'je', 'tu', 'il', 'elle',
    'nous', 'vous', 'ils', 'elles', 'ce', 'cet', 'cette', 'ces',
    'mon', 'ton', 'son', 'ma', 'ta', 'sa', 'mes', 'tes', 'ses',
    'nos', 'vos', 'leurs', 'au', 'aux',
})

_DE_WORDS = frozenset({
    'der', 'die', 'das', 'den', 'dem', 'des', 'ein', 'eine', 'einen',
    'einer', 'einem', 'eines', 'und', 'oder', 'aber', 'sondern',
    'denn', 'doch', 'nicht', 'gar', 'auch', 'als', 'wie', 'bei',
    'mit', 'von', 'aus', 'nach', 'zu', 'ist', 'sind', 'war', 'waren',
    'wird', 'werden', 'hat', 'haben', 'ich', 'du', 'er', 'sie', 'es',
    'wir', 'ihr', 'sie', 'mein', 'dein', 'sein', 'ihr', 'unser',
    'euer', 'mich', 'dich', 'sich',
})


def detect_language(text: str) -> dict[str, Any]:
    if not text.strip():
        return {"language": "unknown", "confidence": 0.0}

    cjk = sum(1 for c in text if '\u4e00' <= c <= '\u9fff')
    cyrillic = sum(1 for c in text if '\u0400' <= c <= '\u04ff')
    arabic = sum(1 for c in text if '\u0600' <= c <= '\u06ff')

    total_letters = sum(1 for c in text if c.isalpha())
    if total_letters == 0:
        return {"language": "unknown", "confidence": 0.0}

    if cjk / total_letters > 0.3:
        return {"language": "zh", "confidence": round(cjk / total_letters, 2)}
    if cyrillic / total_letters > 0.3:
        return {"language": "ru", "confidence": round(cyrillic / total_letters, 2)}
    if arabic / total_letters > 0.3:
        return {"language": "ar", "confidence": round(arabic / total_letters, 2)}

    words = [w.lower() for w in text.split()]

    counts = {
        'en': sum(1 for w in words if w in _EN_WORDS),
        'es': sum(1 for w in words if w in _ES_WORDS),
        'fr': sum(1 for w in words if w in _FR_WORDS),
        'de': sum(1 for w in words if w in _DE_WORDS),
    }

    total_matches = sum(counts.values())
    if total_matches == 0:
        return {"language": "en", "confidence": 0.5}

    best_lang = max(counts, key=counts.get)
    confidence = round(counts[best_lang] / total_matches, 2)

    return {"language": best_lang, "confidence": confidence}
