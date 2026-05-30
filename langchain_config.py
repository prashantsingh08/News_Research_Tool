# ============================================================
# langchain_config.py
# LangChain + OpenAI + NewsAPI Configuration
# ============================================================

import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from newsapi import NewsApiClient
from streamlit import logger

# ── Load environment variables from .env file ──
load_dotenv()

# ── API Keys (set these in .env or replace directly for testing) ──
GROQAI_API_KEY = os.getenv("GROQAI_API_KEY")
NEWSAPI_KEY    = os.getenv("NEWSAPI_KEY")

# ── Initialize GroqAI LLM with fallback models ──────────────────
# List of Groq models optimized for news summarization (newest first)
GROQ_MODELS = "llama-3.3-70b-versatile" 
llm = ChatGroq(
    api_key=GROQAI_API_KEY,
    model_name="llama-3.3-70b-versatile", 
    temperature=0.3, # Lower = more factual, less creative
    max_tokens=1024, # Maximum tokens in the response
)
print("Groq LLM (LLaMA 3 8B) initialised")


# def initialize_llm():
#     """
#     Initialize LLM with primary model, with fallback options.
#     """
#     for model in GROQ_MODELS:
#         try:
#             llm_instance = ChatGroq(
#                 api_key=GROQAI_API_KEY,
#                 model=model,
#                 temperature=0.5,      # 0 = factual, 1 = creative
#                 max_tokens=1500,
#                 timeout=30,
#             )
#             print(f"✓ Successfully initialized LLM with model: {model}")
#             return llm_instance
#         except Exception as e:
#             print(f"⚠ Model {model} failed: {str(e)}")
#             continue
    
#     # If all models fail, raise error
#     raise RuntimeError(f"Failed to initialize any LLM model. Tried: {GROQ_MODELS}")

# llm = initialize_llm()

# ── Prompt Template ────────────────────────────────────────────
template = """
You are an expert AI assistant specialized in analyzing and summarizing news across all domains.

Given the query below and the provided news article summaries, produce a clear, concise, 
and well-structured comprehensive summary.

Guidelines:
1. Synthesize key information from all articles
2. Identify main themes and trends
3. Highlight important facts and developments
4. Note any contrasting viewpoints or updates
5. Include relevant context and implications
6. Keep the summary objective and factual

Query: {query}

News Summaries:
{summaries}

Comprehensive Summary:
"""

prompt = PromptTemplate(
    template=template,
    input_variables=["query", "summaries"],
)

# ── LangChain LLM Chain (using LCEL pipe operator) ────────────
llm_chain = prompt | llm

# ── NewsAPI Client ─────────────────────────────────────────────
newsapi = NewsApiClient(api_key=NEWSAPI_KEY)


def get_news_articles(query: str, max_articles: int = 10) -> list:
    """
    Fetch news articles from NewsAPI for the given query.
    Returns a list of article dicts.
    """
    try:
        response = newsapi.get_everything(
            q=query,
            language="en",
            sort_by="relevancy",
            page_size=max_articles,
        )
        return response.get("articles", [])
    except Exception as e:
        print(f"[NewsAPI Error] {e}")
        return []


def format_articles(articles: list) -> list:
    """
    Format raw articles into clean dicts with title, description, url, source.
    """
    formatted = []
    for art in articles:
        if art.get("description"):  # skip articles with no description
            formatted.append({
                "title":       art.get("title", "No Title"),
                "description": art.get("description", ""),
                "url":         art.get("url", ""),
                "source":      art.get("source", {}).get("name", "Unknown"),
                "published":   art.get("publishedAt", "")[:10],  # date only
            })
    return formatted


def summarize_articles(articles: list) -> str:
    """
    Concatenate article descriptions into one text block for the LLM.
    """
    parts = []
    for i, art in enumerate(articles, 1):
        parts.append(
            f"[Article {i} — {art['source']} | {art['published']}]\n"
            f"Title: {art['title']}\n"
            f"Summary: {art['description']}"
        )
    return "\n\n".join(parts) if parts else "No articles found."


def get_ai_summary(query: str, articles: list) -> str:
    """
    Generate AI summary from fetched articles.
    """

    summaries_text = summarize_articles(articles)

    try:
        result = llm_chain.invoke({
            "query": query,
            "summaries": summaries_text
        })

        # Debug logs
        print(f"Response Type: {type(result)}")

        # LangChain AIMessage response
        if hasattr(result, "content"):
            return result.content.strip()

        # Fallback
        return str(result).strip()

    except Exception as e:
        error_msg = str(e)

        print(f"[LLM Error Details] {error_msg}")

        if "model_decommissioned" in error_msg.lower():
            return (
                "[Error] The AI model needs to be updated. "
                "Please check the configuration and restart the app."
            )

        elif "rate_limit" in error_msg.lower():
            return (
                "[Error] Rate limit reached. "
                "Please wait a moment and try again."
            )

        elif "invalid" in error_msg.lower() and "key" in error_msg.lower():
            return (
                "[Error] Invalid API key. "
                "Please check your .env file configuration."
            )

        return f"[LLM Error] Could not generate summary: {error_msg}"