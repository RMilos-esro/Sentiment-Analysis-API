# app/nlp/sentiment.py
from langdetect import detect, DetectorFactory, LangDetectException
from huggingface_hub import InferenceClient
from app.config import HF_TOKEN

DetectorFactory.seed = 0
client = InferenceClient(token=HF_TOKEN, provider="hf-inference")

MODEL = "nlptown/bert-base-multilingual-uncased-sentiment"

def detect_language(text: str) -> str:
    try:
        return detect(text)
    except LangDetectException:
        return "unknown"

def stars_to_label(label: str) -> str:
    
    stars = int(label[0])
    if stars <= 2:
        return "NEGATIVE"
    elif stars == 3:
        return "NEUTRAL"
    else:
        return "POSITIVE"

def analyze_sentiment_by_lang(text: str) -> dict:
    lang = detect_language(text)

    if lang not in ("es", "en"):
        return {
            "language": lang,
            "supported": False,
            "error": f"'{lang}' not supported. Please send text in English or Spanish."
        }

    result = client.text_classification(text, model=MODEL)[0]  # {"label": "5 stars", "score": ...}

    label = stars_to_label(result["label"])

    return {
        "language": lang,
        "supported": True,
        "label": label,
        "score": round(result["score"], 4)
    }