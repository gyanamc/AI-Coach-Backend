# 🧠 AI-Coach-Backend

A LangGraph-powered backend that combines **Google SERP** search with **LLM reasoning** (OpenAI GPT-4o-mini by default).
Fully compatible with **Open WebUI** via the `/v1/chat/completions` endpoint.

---

## 🚀 Deploy on Railway
1. Push this repo to GitHub.
2. In [Railway.app](https://railway.app):
   - **Create New Project → Deploy from GitHub Repo**
   - Add environment variables:

     ```
     OPENAI_API_KEY=sk-your-key
     GOOGLE_API_KEY=your-serpapi-key
     SERPAPI_ENGINE=google
     MODEL_PROVIDER=openai
     ```

   - Railway auto-detects FastAPI.
   - Start command (already in Procfile):
     ```
     uvicorn app:app --host 0.0.0.0 --port $PORT
     ```

3. Deploy and get your public URL:
