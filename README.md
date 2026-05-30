# 📰 Equity Research News Tool

An AI-powered news research tool built with **LangChain**, **OpenAI**, **NewsAPI**, and **Streamlit**.  
Enter any company or financial topic and get real-time news fetched and summarized by AI instantly.

---

## 🗂️ Project Structure

```
news_research_tool/
│
├── app.py                  # Streamlit frontend (UI)
├── langchain_config.py     # LangChain + OpenAI + NewsAPI logic
├── requirements.txt        # Python dependencies
├── .env.example            # API key template (copy to .env)
└── README.md               # This file
```

---

## ⚙️ Setup Instructions

### Step 1 — Clone or download the project
```bash
git clone https://github.com/your-username/news-research-tool
cd news_research_tool
```

### Step 2 — Install dependencies
```bash
pip install -r requirements.txt
```

### Step 3 — Add your API keys
```bash
cp .env.example .env
```
Then open `.env` and fill in:
```
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxx
NEWSAPI_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### Step 4 — Run the app
```bash
streamlit run app.py
```
The app will open at `http://localhost:8501`

---

## 🔑 Getting API Keys

| Service | Link | Free Tier |
|---------|------|-----------|
| OpenAI | https://platform.openai.com/api-keys | $5 free credits |
| NewsAPI | https://newsapi.org/register | 100 req/day free |

---

## 🚀 How It Works

```
User enters query
      ↓
NewsAPI fetches top 10 relevant articles
      ↓
Article titles + descriptions extracted
      ↓
LangChain formats them into a prompt
      ↓
OpenAI GPT generates a structured summary
      ↓
Streamlit displays summary + article cards
```

---

## 💡 Example Queries
- `Tesla Q1 2024 earnings`
- `RBI monetary policy India`
- `Infosys revenue guidance`
- `US Fed rate cut 2024`
- `Reliance Jio 5G expansion`

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.10+ | Core language |
| Streamlit | Web UI |
| LangChain | LLM orchestration |
| OpenAI GPT | AI summarization |
| NewsAPI | News data source |
| python-dotenv | Secure key management |

---

## 📦 Optional Enhancements (Phase 7)
- [ ] User authentication (Streamlit-Authenticator)
- [ ] Save query history to CSV / SQLite
- [ ] Export summaries as PDF
- [ ] Add sentiment analysis (Positive / Neutral / Negative)
- [ ] Deploy on Streamlit Cloud (free hosting)

---

## 🚢 Deployment (Streamlit Cloud — Free)
1. Push code to GitHub
2. Go to https://share.streamlit.io
3. Connect your repo
4. Add API keys in **Secrets** settings
5. Click **Deploy** — live in 2 minutes!

---

## 👤 Author
Built as part of LLM + Data Science project portfolio.
