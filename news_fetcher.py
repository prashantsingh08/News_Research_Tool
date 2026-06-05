# ============================================================
# news_fetcher.py  —  Multi-source news fetching
# Sources: NewsAPI → GNews → The Guardian → NewsData.io
# ============================================================

import os
import requests
from datetime import date, datetime
from newsapi import NewsApiClient
from languages import NEWSAPI_SUPPORTED

# ── API Keys ───────────────────────────────────────────────────
NEWSAPI_KEY     = os.getenv("NEWSAPI_KEY", "")
GNEWSAPI_KEY    = os.getenv("GNEWSAPI_KEY", "")
THEGUARDIAN_KEY = os.getenv("THEGUARDIAN_KEY", "")
NEWSDATA_KEY    = os.getenv("NEWSDATA_KEY", "")

# ── NewsAPI categories ─────────────────────────────────────────
CATEGORIES = [
    "🔍 All",
    "💼 Business",
    "🎭 Entertainment",
    "🏥 Health",
    "🔬 Science",
    "⚽ Sports",
    "💻 Technology",
    "🌍 General / Politics",
    "🌦️ Weather & Environment",
    "💥 Disasters & Crisis",
    "📜 Policy & Governance",
]

# Internal mapping → NewsAPI category string
CATEGORY_MAP = {
    "🔍 All":                   "",
    "💼 Business":              "business",
    "🎭 Entertainment":         "entertainment",
    "🏥 Health":                "health",
    "🔬 Science":               "science",
    "⚽ Sports":                "sports",
    "💻 Technology":            "technology",
    "🌍 General / Politics":    "general",
    "🌦️ Weather & Environment": "",     # use keyword search
    "💥 Disasters & Crisis":    "",
    "📜 Policy & Governance":   "",
}

# Extra keywords to append for special categories
CATEGORY_KEYWORDS = {
    "🌦️ Weather & Environment": "weather OR climate OR environment OR flood OR storm",
    "💥 Disasters & Crisis":    "disaster OR earthquake OR flood OR hurricane OR crisis OR emergency",
    "📜 Policy & Governance":   "policy OR government OR parliament OR legislation OR law OR regulation",
}


def _clean(art: dict) -> dict | None:
    """Normalize a raw article dict. Returns None for junk entries."""
    title = (art.get("title") or "").strip()
    desc  = (art.get("description") or art.get("content") or "").strip()
    url   = (art.get("url") or "").strip()
    if not title or not desc or "[Removed]" in title or not url:
        return None
    return {
        "title":       title[:200],
        "description": desc[:600],
        "url":         url,
        "source":      art.get("source_name") or art.get("source", {}).get("name", "Unknown"),
        "published":   (art.get("publishedAt") or art.get("published_at") or
                        art.get("pubDate") or "")[:10],
        "image":       art.get("urlToImage") or art.get("image") or "",
    }


# ══════════════════════════════════════════════════════════════
# SOURCE 1: NewsAPI
# ══════════════════════════════════════════════════════════════
def fetch_newsapi(
    query: str,
    lang_code: str,
    category_label: str,
    from_date: str,
    to_date: str,
    max_articles: int,
    sort_by: str = "relevancy",
) -> list[dict]:
    if not NEWSAPI_KEY:
        return []

    lang = lang_code if lang_code in NEWSAPI_SUPPORTED else "en"
    cat  = CATEGORY_MAP.get(category_label, "")
    kw   = CATEGORY_KEYWORDS.get(category_label, "")
    full_query = f"{query} {kw}".strip() if kw else query

    try:
        client = NewsApiClient(api_key=NEWSAPI_KEY)

        if cat and not full_query:
            # Category browse (top-headlines)
            resp = client.get_top_headlines(
                category=cat, language=lang, page_size=max_articles
            )
        elif cat:
            resp = client.get_everything(
                q=full_query, language=lang,
                from_param=from_date, to=to_date,
                sort_by=sort_by, page_size=max_articles,
            )
        else:
            resp = client.get_everything(
                q=full_query, language=lang,
                from_param=from_date, to=to_date,
                sort_by=sort_by, page_size=max_articles,
            )

        raw = resp.get("articles", [])
        results = [_clean(a) for a in raw]
        return [r for r in results if r]
    except Exception as e:
        print(f"[NewsAPI] Error: {e}")
        return []


# ══════════════════════════════════════════════════════════════
# SOURCE 2: GNews
# ══════════════════════════════════════════════════════════════
def fetch_gnews(
    query: str,
    lang_code: str,
    from_date: str,
    to_date: str,
    max_articles: int,
) -> list[dict]:
    if not GNEWSAPI_KEY:
        return []

    kw = query or "world news"
    url = "https://gnews.io/api/v4/search"
    params = {
        "q":        kw,
        "lang":     lang_code,
        "from":     f"{from_date}T00:00:00Z",
        "to":       f"{to_date}T23:59:59Z",
        "max":      min(max_articles, 10),
        "apikey":   GNEWSAPI_KEY,
        "sortby":   "relevance",
    }
    try:
        resp = requests.get(url, params=params, timeout=10)
        data = resp.json()
        raw  = data.get("articles", [])
        cleaned = []
        for a in raw:
            src = a.get("source", {}).get("name", "GNews")
            cleaned.append(_clean({**a, "source_name": src}))
        return [r for r in cleaned if r]
    except Exception as e:
        print(f"[GNews] Error: {e}")
        return []


# ══════════════════════════════════════════════════════════════
# SOURCE 3: The Guardian
# ══════════════════════════════════════════════════════════════
def fetch_guardian(
    query: str,
    from_date: str,
    to_date: str,
    max_articles: int,
) -> list[dict]:
    if not THEGUARDIAN_KEY:
        return []

    url = "https://content.guardianapis.com/search"
    params = {
        "q":            query or "world",
        "from-date":    from_date,
        "to-date":      to_date,
        "page-size":    min(max_articles, 50),
        "api-key":      THEGUARDIAN_KEY,
        "show-fields":  "trailText,thumbnail",
        "order-by":     "relevance",
    }
    try:
        resp = requests.get(url, params=params, timeout=10)
        data = resp.json()
        items = data.get("response", {}).get("results", [])
        results = []
        for a in items:
            fields = a.get("fields", {})
            cleaned = _clean({
                "title":       a.get("webTitle", ""),
                "description": fields.get("trailText", a.get("webTitle", "")),
                "url":         a.get("webUrl", ""),
                "source_name": "The Guardian",
                "publishedAt": a.get("webPublicationDate", "")[:10],
                "urlToImage":  fields.get("thumbnail", ""),
            })
            if cleaned:
                results.append(cleaned)
        return results
    except Exception as e:
        print(f"[Guardian] Error: {e}")
        return []


# ══════════════════════════════════════════════════════════════
# SOURCE 4: NewsData.io
# ══════════════════════════════════════════════════════════════
def fetch_newsdata(
    query: str,
    lang_code: str,
    from_date: str,
    to_date: str,
    max_articles: int,
) -> list[dict]:
    if not NEWSDATA_KEY:
        return []

    url = "https://newsdata.io/api/1/news"
    params = {
        "apikey":    NEWSDATA_KEY,
        "q":         query or "world",
        "language":  lang_code,
        "from_date": from_date,
        "to_date":   to_date,
        "size":      min(max_articles, 10),
    }
    try:
        resp = requests.get(url, params=params, timeout=10)
        data = resp.json()
        raw  = data.get("results", [])
        results = []
        for a in raw:
            cleaned = _clean({
                "title":       a.get("title", ""),
                "description": a.get("description") or a.get("content") or "",
                "url":         a.get("link", ""),
                "source_name": a.get("source_id", "NewsData"),
                "publishedAt": (a.get("pubDate") or "")[:10],
                "urlToImage":  a.get("image_url") or "",
            })
            if cleaned:
                results.append(cleaned)
        return results
    except Exception as e:
        print(f"[NewsData] Error: {e}")
        return []


# ══════════════════════════════════════════════════════════════
# MAIN AGGREGATOR — tries all sources, deduplicates
# ══════════════════════════════════════════════════════════════
def fetch_all_news(
    query: str,
    lang_label: str,
    lang_code: str,
    gnews_lang: str,
    nd_lang: str,
    category_label: str,
    from_date: date,
    to_date: date,
    max_articles: int = 10,
    sort_by: str = "relevancy",
) -> tuple[list[dict], dict]:
    """
    Fetch from all 4 APIs, merge, deduplicate, return articles + source stats.
    Returns: (articles_list, source_counts_dict)
    """
    fd = from_date.strftime("%Y-%m-%d")
    td = to_date.strftime("%Y-%m-%d")

    # Fetch from each source
    newsapi_arts  = fetch_newsapi(query, lang_code, category_label, fd, td, max_articles, sort_by)
    gnews_arts    = fetch_gnews(query, gnews_lang, fd, td, max_articles)
    guardian_arts = fetch_guardian(query, fd, td, max_articles)
    newsdata_arts = fetch_newsdata(query, nd_lang, fd, td, max_articles)

    source_counts = {
        "NewsAPI":      len(newsapi_arts),
        "GNews":        len(gnews_arts),
        "The Guardian": len(guardian_arts),
        "NewsData.io":  len(newsdata_arts),
    }

    # Merge and deduplicate by URL
    all_arts: list[dict] = []
    seen_urls: set[str] = set()
    seen_titles: set[str] = set()

    for art in newsapi_arts + gnews_arts + guardian_arts + newsdata_arts:
        url   = art["url"]
        title = art["title"].lower()[:80]
        if url in seen_urls or title in seen_titles:
            continue
        seen_urls.add(url)
        seen_titles.add(title)
        all_arts.append(art)

    return all_arts, source_counts
