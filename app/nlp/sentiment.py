# app/nlp/sentiment.py
from langdetect import detect, DetectorFactory, LangDetectException
from huggingface_hub import InferenceClient
from app.config import HF_TOKEN

DetectorFactory.seed = 0
client = InferenceClient(token=HF_TOKEN, provider="hf-inference")

SPANISH_LABEL_MAP = {"POS": "POSITIVE", "NEG": "NEGATIVE", "NEU": "NEUTRAL"}

MODEL_ES = "pysentimiento/robertuito-sentiment-analysis"
MODEL_EN = "distilbert-base-uncased-finetuned-sst-2-english"

def detect_language(text: str) -> str:
    try:
        return detect(text)
    except LangDetectException:
        return "unknown"

def analyze_sentiment_by_lang(text: str) -> dict:
    lang = detect_language(text)

    if lang not in ("es", "en"):
        return {
            "language": lang,
            "supported": False,
            "error": f"'{lang}' not supported. Please send text in English or Spanish."
        }

    model = MODEL_ES if lang == "es" else MODEL_EN
    result = client.text_classification(text, model=model)[0]  # {"label": ..., "score": ...}

    label = result["label"]
    if lang == "es" and label in SPANISH_LABEL_MAP:
        label = SPANISH_LABEL_MAP[label]

    return {
        "language": lang,
        "supported": True,
        "label": label,
        "score": round(result["score"], 4)
    }