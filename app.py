# ============================================================
# app.py  —  News Research Tool (Complete)
# Features:
#   ✅ Dark / Light theme toggle (top-right, no page reload)
#   ✅ 24 language selector + detect language from search query
#   ✅ Language change translates EXISTING summary (no re-search)
#   ✅ Date range picker
#   ✅ News category filter (sports, health, politics, etc.)
#   ✅ 4 news sources (NewsAPI + GNews + Guardian + NewsData)
#   ✅ Stats cards (articles, sources, model, word count)
#   ✅ PDF and TXT download
#   ✅ Toggle to show/hide articles
#   ✅ Sort-by option
# ============================================================

import streamlit as st
from dotenv import load_dotenv
from datetime import date, timedelta

load_dotenv()

# ── Internal modules ────────────────────────────────────────────
from languages      import LANGUAGES, detect_language_from_query, strip_language_from_query
from news_fetcher   import fetch_all_news, CATEGORIES
from langchain_config import generate_summary, get_model_name
from translator     import translate
from pdf_generator  import generate_pdf, generate_txt

# ══════════════════════════════════════════════════════════════
# PAGE CONFIG (must be first Streamlit call)
# ══════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="📰 News Research Tool",
    page_icon="📰",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════════
# SESSION STATE DEFAULTS
# ══════════════════════════════════════════════════════════════
defaults = {
    "dark_mode":        False,
    "articles":         [],
    "source_counts":    {},
    "english_summary":  "",
    "final_summary":    "",
    "last_query":       "",
    "searched":         False,
    "lang_label":       "🇺🇸 English",
    "show_articles":    True,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ══════════════════════════════════════════════════════════════
# THEME CSS (injected dynamically — no page reload)
# ══════════════════════════════════════════════════════════════
LIGHT_CSS = """
:root {
    --bg:        #FFFFFF;
    --bg2:       #F0F4F8;
    --bg3:       #EAF1FB;
    --text:      #1A1A1A;
    --text2:     #555555;
    --accent:    #2E75B6;
    --navy:      #1B3A6B;
    --border:    #D0DCF0;
    --card-bg:   #F8FAFD;
    --card-bdr:  #2E75B6;
    --success:   #28a745;
    --warn:      #ffc107;
}
"""

DARK_CSS = """
:root {
    --bg:        #0E1117;
    --bg2:       #1A1F2E;
    --bg3:       #1E2A3A;
    --text:      #E8EAF0;
    --text2:     #A0A8B8;
    --accent:    #4A9EDB;
    --navy:      #7CB9E8;
    --border:    #2D3A50;
    --card-bg:   #1A2030;
    --card-bdr:  #4A9EDB;
    --success:   #2EA44F;
    --warn:      #D29922;
}
"""

COMMON_CSS = """
/* ── Global ── */
body, .stApp {
    background-color: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'Inter', -apple-system, sans-serif;
}
[data-testid="stSidebar"] {
    background-color: var(--bg2) !important;
    border-right: 1px solid var(--border);
}
/* ── Cards ── */
.stat-card {
    background: var(--bg3);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 14px 18px;
    text-align: center;
    margin-bottom: 8px;
}
.stat-value { font-size: 26px; font-weight: 700; color: var(--accent); margin: 0; }
.stat-label { font-size: 12px; color: var(--text2); margin: 4px 0 0; }
.stat-sub   { font-size: 11px; color: var(--text2); }
/* ── Summary box ── */
.summary-box {
    background: var(--bg3);
    border: 1.5px solid var(--border);
    border-left: 5px solid var(--accent);
    border-radius: 10px;
    padding: 22px 26px;
    font-size: 15px;
    line-height: 1.85;
    color: var(--text);
    white-space: pre-wrap;
    margin-bottom: 16px;
}
/* ── Article card ── */
.art-card {
    background: var(--card-bg);
    border-left: 4px solid var(--card-bdr);
    border-radius: 8px;
    padding: 14px 18px;
    margin-bottom: 10px;
}
.art-title  { font-size: 14px; font-weight: 600; color: var(--navy); margin-bottom: 4px; }
.art-meta   { font-size: 12px; color: var(--text2); margin-bottom: 6px; }
.art-desc   { font-size: 13px; color: var(--text); line-height: 1.55; }
/* ── Theme toggle button ── */
.theme-toggle-wrap {
    position: fixed;
    top: 14px;
    right: 80px;
    z-index: 9999;
}
.theme-btn {
    background: var(--bg3);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 5px 14px;
    font-size: 13px;
    cursor: pointer;
    color: var(--text);
}
/* ── Source badge ── */
.src-badge {
    display: inline-block;
    background: var(--bg3);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 2px 10px;
    font-size: 11px;
    color: var(--text2);
    margin: 2px;
}
/* ── Headings ── */
h1,h2,h3,h4 { color: var(--navy) !important; }
/* ── Streamlit overrides ── */
.stTextInput input, .stSelectbox select, .stDateInput input {
    background: var(--bg2) !important;
    color: var(--text) !important;
    border-color: var(--border) !important;
}
.stButton > button {
    background-color: var(--accent) !important;
    color: white !important;
    border: none !important;
    border-radius: 6px;
}
.stButton > button:hover { opacity: 0.88; }
div[data-testid="metric-container"] {
    background: var(--bg3);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 10px;
}
"""

def inject_css():
    theme_vars = DARK_CSS if st.session_state.dark_mode else LIGHT_CSS
    st.markdown(
        f"<style>{theme_vars}{COMMON_CSS}</style>",
        unsafe_allow_html=True,
    )

inject_css()

# ══════════════════════════════════════════════════════════════
# THEME TOGGLE  (top-right fixed position)
# ══════════════════════════════════════════════════════════════
icon  = "🌙 Dark" if not st.session_state.dark_mode else "☀️ Light"
label = f"Switch to {icon} Mode"

# Use a small column trick to put the toggle at the top right
_c1, _c2 = st.columns([9, 1])
with _c2:
    if st.button(icon, key="theme_btn", help="Toggle dark/light theme"):
        st.session_state.dark_mode = not st.session_state.dark_mode
        inject_css()
        st.rerun()

# ══════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("## ⚙️ Settings")
    st.markdown("---")

    # ── Language ───────────────────────────────────────────────
    st.markdown("### 🌐 Language")
    lang_options = list(LANGUAGES.keys())
    current_idx  = lang_options.index(st.session_state.lang_label) \
                   if st.session_state.lang_label in lang_options else 0

    selected_lang = st.selectbox(
        "Output language",
        lang_options,
        index=current_idx,
        key="lang_selector",
        label_visibility="collapsed",
    )

    # Detect language change — translate WITHOUT re-searching
    if selected_lang != st.session_state.lang_label:
        st.session_state.lang_label = selected_lang
        # Re-translate existing summary
        if st.session_state.english_summary:
            tgt = LANGUAGES[selected_lang]["tr"]
            with st.spinner(f"🌐 Translating to {selected_lang}..."):
                st.session_state.final_summary = translate(
                    st.session_state.english_summary, tgt
                )
        st.rerun()

    st.markdown("---")

    # ── Category ───────────────────────────────────────────────
    st.markdown("### 📂 Category")
    category = st.selectbox(
        "Category", CATEGORIES, index=0, label_visibility="collapsed"
    )

    st.markdown("---")

    # ── Date range ─────────────────────────────────────────────
    st.markdown("### 📅 Date Range")
    col_d1, col_d2 = st.columns(2)
    with col_d1:
        from_date = st.date_input(
            "From", value=date.today() - timedelta(days=7),
            max_value=date.today(), label_visibility="collapsed",
        )
    with col_d2:
        to_date = st.date_input(
            "To", value=date.today(),
            max_value=date.today(), label_visibility="collapsed",
        )

    st.markdown("---")

    # ── Sort & Count ───────────────────────────────────────────
    st.markdown("### 🔃 Sort By")
    sort_by = st.selectbox(
        "Sort", ["relevancy", "publishedAt", "popularity"],
        label_visibility="collapsed",
    )

    st.markdown("### 📄 Articles per source")
    max_articles = st.slider("", 3, 15, 8, label_visibility="collapsed")

    st.markdown("---")

    # ── Display toggles ────────────────────────────────────────
    st.markdown("### 🖥️ Display")
    st.session_state.show_articles = st.toggle(
        "Show source articles", value=st.session_state.show_articles
    )
    show_en = st.checkbox("Also show English summary", value=False)

    st.markdown("---")
    st.caption(f"🤖 Model: `{get_model_name()}`")
    st.caption("Sources: NewsAPI · GNews · Guardian · NewsData")

# ══════════════════════════════════════════════════════════════
# MAIN AREA
# ══════════════════════════════════════════════════════════════
st.markdown("# 📰 News Research Tool")
theme_hint = "🌙 dark" if st.session_state.dark_mode else "☀️ light"
st.markdown(
    f"Search **any news topic worldwide** — politics, sports, health, tech, "
    f"entertainment, weather, disasters & more.  "
    f"Now in **{st.session_state.lang_label}** · Theme: {theme_hint}"
)
st.markdown("---")

# ── Search bar ─────────────────────────────────────────────────
col_q, col_btn = st.columns([5, 1])
with col_q:
    raw_query = st.text_input(
        "Search",
        placeholder=(
            "e.g.  IPL 2024  |  Ukraine war  |  Apple iPhone  |  "
            "Climate change  |  'Show in Hindi'  |  Budget 2025 India ..."
        ),
        label_visibility="collapsed",
        key="search_input",
    )
with col_btn:
    search_clicked = st.button("🔍 Search", use_container_width=True, type="primary")

# ── Example queries ────────────────────────────────────────────
if not st.session_state.searched:
    st.markdown("#### 💡 Example queries:")
    eg_cols = st.columns(4)
    examples = [
        "IPL 2024 cricket", "Ukraine Russia war", "Apple earnings 2024",
        "COVID vaccine news", "India budget 2025", "ChatGPT AI news",
        "Champions League", "Climate change India",
    ]
    for col, ex in zip(eg_cols * 2, examples):
        col.code(ex, language=None)
    st.markdown("---")

# ══════════════════════════════════════════════════════════════
# SEARCH LOGIC
# ══════════════════════════════════════════════════════════════
if search_clicked and raw_query.strip():

    # ── Detect language from query text ───────────────────────
    detected_lang = detect_language_from_query(raw_query)
    if detected_lang:
        st.session_state.lang_label = detected_lang
        selected_lang = detected_lang

    clean_query = strip_language_from_query(raw_query)

    lang_info   = LANGUAGES[st.session_state.lang_label]
    lang_code   = lang_info["tr"]
    gnews_lang  = lang_info["gnews"]
    nd_lang     = lang_info["nd"]

    # ── Fetch articles ─────────────────────────────────────────
    with st.spinner(f"🔍 Fetching news from 4 sources for **\"{clean_query}\"** ..."):
        articles, source_counts = fetch_all_news(
            query=clean_query,
            lang_label=st.session_state.lang_label,
            lang_code=lang_code,
            gnews_lang=gnews_lang,
            nd_lang=nd_lang,
            category_label=category,
            from_date=from_date,
            to_date=to_date,
            max_articles=max_articles,
            sort_by=sort_by,
        )

    if not articles:
        st.error(
            "❌ No articles found. Try:\n"
            "- Different keywords or broader terms\n"
            "- Changing the date range\n"
            "- Switching category to '🔍 All'\n"
            "- Checking your API keys in `.env`"
        )
        st.stop()

    st.session_state.articles      = articles
    st.session_state.source_counts = source_counts

    # ── Generate AI summary ────────────────────────────────────
    with st.spinner("🤖 AI is reading and summarizing the articles..."):
        en_summary = generate_summary(clean_query, articles, source_counts)

    st.session_state.english_summary = en_summary
    st.session_state.last_query      = clean_query

    # ── Translate if needed ────────────────────────────────────
    if lang_code != "en":
        with st.spinner(f"🌐 Translating summary to {st.session_state.lang_label}..."):
            final = translate(en_summary, lang_code)
    else:
        final = en_summary

    st.session_state.final_summary = final
    st.session_state.searched      = True

# ══════════════════════════════════════════════════════════════
# RESULTS DISPLAY  (renders from session_state, no re-search)
# ══════════════════════════════════════════════════════════════
if st.session_state.searched and st.session_state.articles:

    articles      = st.session_state.articles
    source_counts = st.session_state.source_counts
    final_summary = st.session_state.final_summary
    en_summary    = st.session_state.english_summary
    query_display = st.session_state.last_query

    total_arts  = len(articles)
    word_count  = len(final_summary.split())
    active_srcs = sum(1 for c in source_counts.values() if c > 0)

    # ── Stat cards ─────────────────────────────────────────────
    st.success(f"✅ Found **{total_arts} articles** from {active_srcs} sources. Summary ready in **{st.session_state.lang_label}**.")
    st.markdown("---")
    st.markdown("### 📊 Stats")

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.markdown(f'<div class="stat-card"><p class="stat-value">{total_arts}</p><p class="stat-label">Total Articles</p></div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="stat-card"><p class="stat-value">{active_srcs}</p><p class="stat-label">News Sources</p></div>', unsafe_allow_html=True)
    c3.markdown(f'<div class="stat-card"><p class="stat-value">{word_count}</p><p class="stat-label">Summary Words</p></div>', unsafe_allow_html=True)
    c4.markdown(f'<div class="stat-card"><p class="stat-value">llama-3.3</p><p class="stat-label">AI Model (Groq)</p><p class="stat-sub">70b-versatile</p></div>', unsafe_allow_html=True)
    c5.markdown(f'<div class="stat-card"><p class="stat-value">{st.session_state.lang_label.split()[1] if len(st.session_state.lang_label.split())>1 else "EN"}</p><p class="stat-label">Output Language</p></div>', unsafe_allow_html=True)

    # Source breakdown
    st.markdown("**Sources breakdown:** " + "  ".join(
        f'<span class="src-badge">{s}: {c}</span>'
        for s, c in source_counts.items() if c > 0
    ), unsafe_allow_html=True)

    st.markdown("---")

    # ── Summary ────────────────────────────────────────────────
    st.markdown(f"### 🧠 AI Summary — {st.session_state.lang_label}")
    formatted = final_summary.replace("\n", "<br>")
    st.markdown(f'<div class="summary-box">{formatted}</div>', unsafe_allow_html=True)

    if show_en and lang_code != "en":
        with st.expander("📄 View original English summary"):
            st.markdown(en_summary)

    # ── Downloads ──────────────────────────────────────────────
    st.markdown("### ⬇️ Download Summary")
    dl1, dl2, dl3 = st.columns(3)

    # TXT
    txt_data = generate_txt(
        query=query_display, summary=final_summary,
        articles=articles, language=st.session_state.lang_label,
        source_counts=source_counts, model_name=get_model_name(),
    )
    with dl1:
        st.download_button(
            "📄 Download .txt",
            data=txt_data,
            file_name=f"news_{query_display[:20].replace(' ','_')}.txt",
            mime="text/plain",
            use_container_width=True,
        )

    # PDF
    try:
        pdf_data = generate_pdf(
            query=query_display, summary=en_summary,  # PDF uses English (font compat)
            articles=articles, language=st.session_state.lang_label,
            source_counts=source_counts, model_name=get_model_name(),
        )
        with dl2:
            st.download_button(
                "📕 Download .pdf",
                data=pdf_data,
                file_name=f"news_{query_display[:20].replace(' ','_')}.pdf",
                mime="application/pdf",
                use_container_width=True,
            )
    except Exception as e:
        with dl2:
            st.caption(f"PDF error: {e}")

    # JSON
    import json
    json_data = json.dumps({
        "query": query_display, "language": st.session_state.lang_label,
        "summary": final_summary, "articles": articles,
        "source_counts": source_counts, "model": get_model_name(),
    }, indent=2, ensure_ascii=False)
    with dl3:
        st.download_button(
            "🗂️ Download .json",
            data=json_data,
            file_name=f"news_{query_display[:20].replace(' ','_')}.json",
            mime="application/json",
            use_container_width=True,
        )

    # ── Articles ───────────────────────────────────────────────
    if st.session_state.show_articles:
        st.markdown("---")
        st.markdown(f"### 📄 Source Articles ({total_arts})")
        for i, art in enumerate(articles, 1):
            with st.expander(f"📌 {i}. {art['title'][:90]} — {art['source']}"):
                st.markdown(f"""
<div class="art-card">
  <div class="art-title">{art['title']}</div>
  <div class="art-meta">📡 {art['source']} &nbsp;|&nbsp; 🗓️ {art['published']}</div>
  <div class="art-desc">{art['description']}</div>
</div>""", unsafe_allow_html=True)
                st.markdown(f"[🔗 Read full article →]({art['url']})")
