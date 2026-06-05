# 📰 News Research Tool — Complete LLM Project

> AI-powered multilingual news summarizer using Groq LLaMA 3.3, 4 news APIs, and Streamlit.

---

## 📁 Project Structure

```
news_research_tool/
│
├── app.py                  ← Main Streamlit UI
├── langchain_config.py     ← Groq LLM + LangChain summarization
├── news_fetcher.py         ← 4 news API integration (NewsAPI, GNews, Guardian, NewsData)
├── translator.py           ← Multilingual translation (deep-translator)
├── pdf_generator.py        ← PDF + TXT export
├── languages.py            ← 24 language config + query detection
│
├── .streamlit/
│   └── config.toml         ← Base Streamlit theme
│
├── .env                    ← Your API keys (pre-filled)
├── .gitignore
├── requirements.txt
├── setup.sh                ← One-click setup (Mac/Linux)
├── setup.bat               ← One-click setup (Windows)
└── README.md
```

---

## ⚡ Quick Start

### Mac / Linux
```bash
bash setup.sh
source venv/bin/activate
streamlit run app.py
```

### Windows
```
setup.bat
venv\Scripts\activate
streamlit run app.py
```

App opens at → **http://localhost:8501**

---

## ✨ Features

| Feature | Details |
|---------|---------|
| 🤖 AI Summarization | Groq LLaMA 3.3-70b (free, ultra-fast) |
| 📡 4 News Sources | NewsAPI + GNews + The Guardian + NewsData.io |
| 🌐 24 Languages | Hindi, Urdu, Japanese, Mandarin, Spanish + more |
| 🗣️ Smart Query | Type "show in Hindi" — auto-detects language |
| 🔄 No Re-search | Language switch translates existing summary only |
| 📅 Date Range | Filter news by custom date range |
| 📂 Categories | Sports, Politics, Health, Tech, Environment, Disasters |
| 🌙 Dark/Light | Theme toggle at top-right (no page reload) |
| 🔘 Article Toggle | Show/hide source articles with toggle switch |
| ⬇️ Export | Download as PDF, TXT, or JSON |
| 📊 Stats Cards | Articles count, sources, word count, model info |

---

## 🌐 Supported Languages (24)

English · Spanish · Portuguese · German · Dutch · Russian ·
Japanese · Korean · Mandarin · French · Italian · Arabic ·
Swedish · Norwegian · Polish · Turkish ·
Hindi · Urdu · Bengali · Tamil · Telugu · Marathi · Gujarati ·
Kannada · Malayalam · Punjabi

**Two ways to select language:**
1. Sidebar dropdown → instantly re-translates without re-searching
2. Type in query: `"Ukraine war in Hindi"` → auto-detects Hindi

---

## 🔎 News Categories

- 🔍 All (default)
- 💼 Business
- 🎭 Entertainment
- 🏥 Health
- 🔬 Science
- ⚽ Sports
- 💻 Technology
- 🌍 General / Politics
- 🌦️ Weather & Environment
- 💥 Disasters & Crisis
- 📜 Policy & Governance

---

## 🤖 AI Model

| Setting | Value |
|---------|-------|
| Provider | Groq (free) |
| Model | llama-3.3-70b-versatile |
| Temperature | 0.3 (factual) |
| Max tokens | 1800 |

---

## 🔑 API Keys (pre-configured in .env)

| Service | Key | Free Limit |
|---------|-----|-----------|
| Groq | GROQAI_API_KEY | Generous free tier |
| NewsAPI | NEWSAPI_KEY | 100 req/day |
| GNews | GNEWSAPI_KEY | 100 req/day |
| The Guardian | THEGUARDIAN_KEY | Unlimited (free) |
| NewsData.io | NEWSDATA_KEY | 200 req/day |

---

## 🚢 Deploy Free on Streamlit Cloud

1. Push to GitHub (exclude `.env` via `.gitignore`)
2. Go to https://share.streamlit.io
3. Connect your repo → select `app.py`
4. Add secrets (Settings → Secrets):
```toml
GROQAI_API_KEY = "gsk_..."
NEWSAPI_KEY = "..."
GNEWSAPI_KEY = "..."
THEGUARDIAN_KEY = "..."
NEWSDATA_KEY = "..."
```
5. Click **Deploy** → live in 2 minutes!

---

## 🐛 Bugs Fixed from Original Code

| Bug | Fix |
|-----|-----|
| `result.strip()` crashed (AIMessage object) | Fixed to `result.content.strip()` |
| `language="en"` hardcoded | Now dynamic from user selection |
| `from streamlit import logger` unused | Removed |
| Language change triggered re-search | Fixed: translates stored summary only |
| Single news source | Now uses 4 APIs with deduplication |
