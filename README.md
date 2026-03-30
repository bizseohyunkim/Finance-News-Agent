## Live Demo
[Finance News Intelligence Agent](https://finance-news-agent-여기에URL.streamlit.app)

---

# Finance News Intelligence Agent

AI-powered financial news aggregation and summarization agent.  
실시간 금융 뉴스를 수집하고 AI로 요약 및 시장 심리를 분석하는 에이전트입니다.

---

## Overview

This agent automatically fetches financial news from RSS feeds, summarizes each article in Korean using Gemini, and provides an overall market sentiment analysis.

Reuters, Yahoo Finance, Bloomberg 등 주요 금융 뉴스 소스에서 실시간으로 뉴스를 수집하고, Gemini 1.5를 활용해 한국어 요약 및 시장 심리 분석을 제공합니다.

---

## Features

- Real-time news fetching from multiple RSS sources (Reuters, Yahoo Finance, Bloomberg, CNBC)
- AI-powered Korean summarization per article
- Overall market sentiment analysis (Bullish / Neutral / Bearish)
- Key themes and risk factor extraction
- Professional financial dashboard UI

---

## Architecture
```
RSS Feed → feedparser → News List
                              ↓
              LangChain Agent → Gemini 1.5 Flash
                              ↓
            Article Summary + Market Sentiment → Streamlit UI
```

---

## Tech Stack

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?style=flat&logo=langchain&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![Google Gemini](https://img.shields.io/badge/Gemini_1.5-4285F4?style=flat&logo=google&logoColor=white)

---

## How to Run
```bash
git clone https://github.com/bizseohyunkim/Finance-News-Agent-.git
cd Finance-News-Agent-
pip install requests beautifulsoup4 feedparser python-dotenv streamlit langchain-google-genai
```

Create `.env` file:
```
GOOGLE_API_KEY=your_gemini_api_key_here
```

Run:
```bash
streamlit run app.py
```

---

## Note

- Gemini API key required (Google AI Studio — free tier available)
- `.env` file is excluded from version control
- Free tier has daily request limits
