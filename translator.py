# ============================================================
# translator.py  —  Translation using deep-translator (free)
# No API key needed — uses Google Translate under the hood
# ============================================================

from deep_translator import GoogleTranslator


def translate(text: str, target_code: str) -> str:
    """
    Translate English text to the target language.
    Splits into 4500-char chunks to respect Google's limit.
    Returns original text if translation fails or target is English.
    """
    if not text or target_code == "en":
        return text

    try:
        # Split into safe chunks
        chunks = [text[i:i + 4500] for i in range(0, len(text), 4500)]
        translated = []
        for chunk in chunks:
            t = GoogleTranslator(source="en", target=target_code).translate(chunk)
            translated.append(t if t else chunk)
        return "\n".join(translated)
    except Exception as e:
        print(f"[Translator] Error translating to '{target_code}': {e}")
        return text + f"\n\n[⚠️ Translation to '{target_code}' failed: {e}]"
