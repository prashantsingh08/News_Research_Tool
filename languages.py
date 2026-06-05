# ============================================================
# languages.py  —  Supported languages configuration
# ============================================================

# Display label → {translation_code, newsapi_code, gnews_code, newsdata_code}
LANGUAGES: dict[str, dict] = {
    "🇺🇸 English":              {"tr": "en",    "newsapi": "en", "gnews": "en", "nd": "en"},
    "🇪🇸 Spanish":              {"tr": "es",    "newsapi": "es", "gnews": "es", "nd": "es"},
    "🇵🇹 Portuguese":           {"tr": "pt",    "newsapi": "pt", "gnews": "pt", "nd": "pt"},
    "🇩🇪 German":               {"tr": "de",    "newsapi": "de", "gnews": "de", "nd": "de"},
    "🇳🇱 Dutch":                {"tr": "nl",    "newsapi": "nl", "gnews": "nl", "nd": "nl"},
    "🇷🇺 Russian":              {"tr": "ru",    "newsapi": "ru", "gnews": "ru", "nd": "ru"},
    "🇯🇵 Japanese":             {"tr": "ja",    "newsapi": "jp", "gnews": "ja", "nd": "ja"},
    "🇰🇷 Korean":               {"tr": "ko",    "newsapi": "en", "gnews": "ko", "nd": "ko"},
    "🇨🇳 Mandarin (Chinese)":   {"tr": "zh-CN", "newsapi": "zh", "gnews": "zh", "nd": "zh"},
    "🇫🇷 French":               {"tr": "fr",    "newsapi": "fr", "gnews": "fr", "nd": "fr"},
    "🇮🇹 Italian":              {"tr": "it",    "newsapi": "it", "gnews": "it", "nd": "it"},
    "🇸🇦 Arabic":               {"tr": "ar",    "newsapi": "ar", "gnews": "ar", "nd": "ar"},
    "🇸🇪 Swedish":              {"tr": "sv",    "newsapi": "sv", "gnews": "sv", "nd": "sv"},
    "🇳🇴 Norwegian":            {"tr": "no",    "newsapi": "no", "gnews": "no", "nd": "no"},
    "🇵🇱 Polish":               {"tr": "pl",    "newsapi": "en", "gnews": "pl", "nd": "pl"},
    "🇹🇷 Turkish":              {"tr": "tr",    "newsapi": "en", "gnews": "tr", "nd": "tr"},
    # ── Indian languages ──────────────────────────────────────
    "🇮🇳 Hindi":                {"tr": "hi",    "newsapi": "en", "gnews": "hi", "nd": "hi"},
    "🇮🇳 Urdu":                 {"tr": "ur",    "newsapi": "en", "gnews": "ur", "nd": "ur"},
    "🇮🇳 Bengali":              {"tr": "bn",    "newsapi": "en", "gnews": "bn", "nd": "bn"},
    "🇮🇳 Tamil":                {"tr": "ta",    "newsapi": "en", "gnews": "ta", "nd": "ta"},
    "🇮🇳 Telugu":               {"tr": "te",    "newsapi": "en", "gnews": "te", "nd": "te"},
    "🇮🇳 Marathi":              {"tr": "mr",    "newsapi": "en", "gnews": "mr", "nd": "mr"},
    "🇮🇳 Gujarati":             {"tr": "gu",    "newsapi": "en", "gnews": "gu", "nd": "gu"},
    "🇮🇳 Kannada":              {"tr": "kn",    "newsapi": "en", "gnews": "kn", "nd": "kn"},
    "🇮🇳 Malayalam":            {"tr": "ml",    "newsapi": "en", "gnews": "ml", "nd": "ml"},
    "🇮🇳 Punjabi":              {"tr": "pa",    "newsapi": "en", "gnews": "pa", "nd": "pa"},
}

# ── NewsAPI supported language codes ──────────────────────────
NEWSAPI_SUPPORTED = {"ar","de","en","es","fr","he","it","nl","no","pt","ru","sv","zh"}

# ── Detect language from free-text prompt ─────────────────────
LANG_KEYWORDS: dict[str, str] = {
    "hindi": "🇮🇳 Hindi",         "हिंदी": "🇮🇳 Hindi",
    "urdu": "🇮🇳 Urdu",           "اردو": "🇮🇳 Urdu",
    "spanish": "🇪🇸 Spanish",     "español": "🇪🇸 Spanish",
    "portuguese": "🇵🇹 Portuguese","português": "🇵🇹 Portuguese",
    "german": "🇩🇪 German",       "deutsch": "🇩🇪 German",
    "dutch": "🇳🇱 Dutch",         "nederlands": "🇳🇱 Dutch",
    "russian": "🇷🇺 Russian",     "русский": "🇷🇺 Russian",
    "japanese": "🇯🇵 Japanese",   "日本語": "🇯🇵 Japanese",
    "korean": "🇰🇷 Korean",       "한국어": "🇰🇷 Korean",
    "chinese": "🇨🇳 Mandarin (Chinese)", "mandarin": "🇨🇳 Mandarin (Chinese)",
    "french": "🇫🇷 French",       "français": "🇫🇷 French",
    "italian": "🇮🇹 Italian",     "italiano": "🇮🇹 Italian",
    "arabic": "🇸🇦 Arabic",       "عربي": "🇸🇦 Arabic",
    "tamil": "🇮🇳 Tamil",         "தமிழ்": "🇮🇳 Tamil",
    "telugu": "🇮🇳 Telugu",       "తెలుగు": "🇮🇳 Telugu",
    "bengali": "🇮🇳 Bengali",     "বাংলা": "🇮🇳 Bengali",
    "marathi": "🇮🇳 Marathi",     "मराठी": "🇮🇳 Marathi",
    "gujarati": "🇮🇳 Gujarati",   "ગુજરાતી": "🇮🇳 Gujarati",
    "kannada": "🇮🇳 Kannada",     "ಕನ್ನಡ": "🇮🇳 Kannada",
    "malayalam": "🇮🇳 Malayalam", "മലയാളം": "🇮🇳 Malayalam",
    "punjabi": "🇮🇳 Punjabi",     "ਪੰਜਾਬੀ": "🇮🇳 Punjabi",
    "turkish": "🇹🇷 Turkish",
    "polish": "🇵🇱 Polish",
    "swedish": "🇸🇪 Swedish",
    "norwegian": "🇳🇴 Norwegian",
    "english": "🇺🇸 English",
}


def detect_language_from_query(query: str) -> str | None:
    """
    Detect if the user typed a language name in the search query.
    E.g. 'Show news in Hindi' → '🇮🇳 Hindi'
    Returns the language label or None if not detected.
    """
    q_lower = query.lower()
    # patterns: "in hindi", "in spanish", "show in french" etc.
    for keyword, label in LANG_KEYWORDS.items():
        if keyword in q_lower:
            return label
    return None


def strip_language_from_query(query: str) -> str:
    """Remove 'in hindi', 'show in spanish' etc. from the search query."""
    import re
    # Remove common patterns like "in hindi", "show in spanish"
    patterns = [
        r"\b(show\s+)?in\s+(hindi|urdu|spanish|portuguese|german|dutch|russian|"
        r"japanese|korean|chinese|mandarin|french|italian|arabic|tamil|telugu|"
        r"bengali|marathi|gujarati|kannada|malayalam|punjabi|turkish|polish|"
        r"swedish|norwegian|english)\b",
        r"\b(हिंदी|اردو|español|português|deutsch|français|italiano|عربي|"
        r"日本語|한국어|বাংলা|தமிழ்|తెలుగు|मराठी|ગુજરાતી|ಕನ್ನಡ|മലയാളം|ਪੰਜਾਬੀ|русский)\b",
    ]
    result = query
    for p in patterns:
        result = re.sub(p, "", result, flags=re.IGNORECASE).strip()
    return result.strip(" ,.")
