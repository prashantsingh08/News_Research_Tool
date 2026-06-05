# ============================================================
# langchain_config.py  —  Groq LLM + LangChain summarization
# Model: llama-3.3-70b-versatile via Groq (free, fast)
# ============================================================

import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate

load_dotenv()

GROQAI_API_KEY = os.getenv("GROQAI_API_KEY", "")
MODEL_NAME     = "llama-3.3-70b-versatile"

# ── LLM instance ───────────────────────────────────────────────
llm = ChatGroq(
    api_key=GROQAI_API_KEY,
    model_name=MODEL_NAME,
    temperature=0.3,
    max_tokens=1800,
)

# ── Prompt ─────────────────────────────────────────────────────
TEMPLATE = """
You are an expert AI news analyst with deep knowledge across all domains including
politics, sports, business, technology, health, science, entertainment, weather,
environment, disasters, policy, and world affairs.

Your task is to read the provided news articles and generate an ACCURATE, FACTUAL,
and WELL-STRUCTURED summary — just like a senior journalist would write.

STRICT RULES:
- Only use facts from the provided articles. Do NOT invent or assume any details.
- If articles are insufficient, say so honestly.
- Always respond in ENGLISH first (translation happens separately).
- Be objective, balanced, and cite source names where possible.

Structure your response EXACTLY as follows:

## 📌 Key Highlights
(3-5 bullet points of the most critical facts)

## 📰 Full Summary
(2-3 paragraphs synthesizing all articles into a coherent narrative)

## 🔍 Key Takeaways
(3 concise bullet points the reader must remember)

## ⚠️ Important Notes
(Any contradictions between sources, missing data, or caveats — if none, write "None")

---
Query: {query}

News Articles ({count} articles from {sources}):
{summaries}

Your structured news summary:
"""

prompt = PromptTemplate(
    template=TEMPLATE,
    input_variables=["query", "count", "sources", "summaries"],
)

llm_chain = prompt | llm


# ── Build prompt text from articles ───────────────────────────
def build_articles_text(articles: list) -> str:
    if not articles:
        return "No articles available."
    parts = []
    for i, art in enumerate(articles, 1):
        parts.append(
            f"[{i}] SOURCE: {art['source']} | DATE: {art['published']}\n"
            f"    TITLE: {art['title']}\n"
            f"    CONTENT: {art['description']}"
        )
    return "\n\n".join(parts)


# ── Generate AI summary ────────────────────────────────────────
def generate_summary(query: str, articles: list, source_counts: dict) -> str:
    """
    Generate AI summary. Always returns English text.
    BUG-FIXED: uses result.content.strip() (not result.strip())
    """
    articles_text = build_articles_text(articles)
    sources_str   = ", ".join(
        f"{src}({cnt})" for src, cnt in source_counts.items() if cnt > 0
    )

    try:
        result = llm_chain.invoke({
            "query":    query,
            "count":    len(articles),
            "sources":  sources_str,
            "summaries": articles_text,
        })
        # ✅ CRITICAL FIX: .content extracts string from AIMessage
        return result.content.strip()

    except Exception as e:
        err = str(e)
        print(f"[LLM Error] {err}")
        if "rate_limit" in err.lower():
            return "⚠️ Groq rate limit reached. Please wait 30 seconds and try again."
        elif "invalid" in err.lower() and "key" in err.lower():
            return "⚠️ Invalid Groq API key. Please check your .env file."
        elif "model" in err.lower():
            return "⚠️ Model temporarily unavailable. Please try again in a moment."
        return f"⚠️ Could not generate summary: {err}"


def get_model_name() -> str:
    return MODEL_NAME
