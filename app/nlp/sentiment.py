from langdetect import detect, DetectorFactory, LangDetectException
from transformers import pipeline

DetectorFactory.seed = 0
SPANISH_LABEL_MAP = {
    "POS": "POSITIVE",
    "NEG": "NEGATIVE",
    "NEU": "NEUTRAL"
}

# Spanish model (RoBERTuito)
nlp_es = pipeline(
    "sentiment-analysis", 
    model="pysentimiento/robertuito-sentiment-analysis"
)

# English model (DistilBERT)
nlp_en = pipeline(
    "sentiment-analysis", 
    model="distilbert-base-uncased-finetuned-sst-2-english"
)


def detect_language(text: str) -> str:
    """Detects the language of the input text."""
    try:
        lang = detect(text)
        return lang
    except LangDetectException:
        return "unknown"


def analyze_sentiment_by_lang(text: str) -> dict:
    """Detects the language and analyzes the sentiment using the appropriate model."""
    lang = detect_language(text)

    # if spanish
    if lang == "es":
        prediction = nlp_es(text)[0]

    # if english
    elif lang == "en":
        prediction = nlp_en(text)[0]
    else:
        # else fallback
        return {
            "language": lang,
            "supported": False,
            "error": f"'{lang}' not supported. Please send text in English or Spanish."
        }

    if lang == "es" and prediction["label"] in SPANISH_LABEL_MAP:
        prediction["label"] = SPANISH_LABEL_MAP[prediction["label"]]

    return {
        "language": lang,
        "supported": True,
        "label": prediction["label"],  
        "score": round(prediction["score"], 4)  
    }