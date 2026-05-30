# ============================================================
# app.py
# Streamlit Frontend — Equity Research News Tool
# ============================================================

import streamlit as st
from langchain_config import (
    get_news_articles,
    format_articles,
    summarize_articles,
    get_ai_summary,
)

# ── Page Configuration ─────────────────────────────────────────
st.set_page_config(
    page_title="Equity Research News Tool",
    page_icon="📰",
    layout="wide",
)

# ── Sidebar ────────────────────────────────────────────────────
with st.sidebar:
    st.title("⚙️ Settings")
    max_articles = st.slider(
        "Number of articles to fetch",
        min_value=3,
        max_value=20,
        value=8,
        step=1,
    )
    show_articles = st.checkbox("Show individual articles", value=True)
    st.markdown("---")
    st.markdown("**How to use:**")
    st.markdown("1. Enter a company or topic\n2. Click **Get News**\n3. Read the AI summary\n4. Browse individual articles below")
    st.markdown("---")
    st.caption("Powered by LangChain + OpenAI + NewsAPI")

# ── Header ─────────────────────────────────────────────────────
st.title("📰 Research News Tool") 
st.markdown(
    "Enter a company, stock, or financial topic to get the latest "
    "news **fetched and summarized by AI**."
)
st.markdown("---")

# ── Search Bar ─────────────────────────────────────────────────
col1, col2 = st.columns([4, 1])
with col1:
    query = st.text_input(
        label="Search query",
        placeholder="e.g. Tesla earnings, Reliance Industries, SEBI regulations ...",
        label_visibility="collapsed",
    )
with col2:
    search_clicked = st.button("🔍 Get News", use_container_width=True)

# ── Main Logic ─────────────────────────────────────────────────
if search_clicked:
    if not query.strip():
        st.warning("⚠️ Please enter a query before searching.")
    else:
        # ── Step 1: Fetch news ──
        with st.spinner(f'Fetching latest news for **"{query}"** ...'):
            raw_articles  = get_news_articles(query, max_articles=max_articles)
            articles       = format_articles(raw_articles)

        if not articles:
            st.error("❌ No articles found. Try a different query or check your NewsAPI key.")
        else:
            # ── Step 2: AI Summary ──
            with st.spinner("🤖 Generating AI summary ..."):
                ai_summary = get_ai_summary(query, articles)

            # ── Summary Section ──
            st.success(f"✅ Found {len(articles)} articles. Summary ready!")
            st.markdown("## 🧠 AI-Generated Summary")
            st.info(ai_summary)

            st.markdown("---")

            # ── Article Cards ──
            if show_articles:
                st.markdown(f"## 📄 Individual Articles ({len(articles)})")
                for i, art in enumerate(articles, 1):
                    with st.expander(f"📌 {i}. {art['title']} — {art['source']}"):
                        col_a, col_b = st.columns([3, 1])
                        with col_a:
                            st.markdown(f"**{art['description']}**")
                        with col_b:
                            st.caption(f"🗓️ {art['published']}")
                            st.caption(f"📡 {art['source']}")
                        st.markdown(f"[Read full article →]({art['url']})")

# ── Empty State ─────────────────────────────────────────────────
elif not search_clicked:
    st.markdown("### 💡 Example queries to try:")
    examples = [
        "Apple Inc quarterly earnings",
        "RBI interest rate India",
        "Reliance Industries acquisition",
        "US Federal Reserve policy 2024",
        "Infosys revenue growth",
    ]
    cols = st.columns(len(examples))
    for col, ex in zip(cols, examples):
        with col:
            st.code(ex, language=None)

    st.markdown("---")
    st.markdown(
        "📌 **Tip:** The more specific your query, "
        "the better the AI summary. Try including company names, "
        "sectors, or financial terms."
    )
