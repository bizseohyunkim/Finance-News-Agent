import streamlit as st
import feedparser
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage
from datetime import datetime

load_dotenv()

st.set_page_config(
    page_title="Finance News Agent",
    layout="wide"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');
    * { font-family: 'Inter', sans-serif; }
    .stApp { background-color: #f0f2f5; }

    [data-testid="stSidebar"] {
        background-color: #0a1628;
    }
    [data-testid="stSidebar"] * { color: #c8d6e5 !important; }

    .top-bar {
        background: linear-gradient(135deg, #0a1628 0%, #1a3a5c 100%);
        padding: 20px 32px;
        margin: -24px -24px 24px -24px;
        border-bottom: 2px solid #c9a84c;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .top-bar-title { font-size: 18px; font-weight: 600; color: white; }
    .top-bar-sub { font-size: 11px; color: #7f9abd; margin-top: 3px; }
    .top-bar-date { font-size: 11px; color: #7f9abd; text-align: right; }

    .news-card {
        background: white;
        border: 1px solid #e2e8f0;
        border-left: 3px solid #0a1628;
        border-radius: 2px;
        padding: 16px 20px;
        margin-bottom: 12px;
    }
    .news-title {
        font-size: 14px;
        font-weight: 600;
        color: #1a2b4a;
        margin-bottom: 6px;
    }
    .news-meta {
        font-size: 11px;
        color: #a0aec0;
        margin-bottom: 8px;
        letter-spacing: 0.3px;
    }
    .news-summary {
        font-size: 13px;
        color: #4a5568;
        line-height: 1.6;
    }
    .section-label {
        font-size: 10px;
        font-weight: 600;
        letter-spacing: 2px;
        text-transform: uppercase;
        color: #4a6fa5 !important;
        margin-bottom: 8px;
    }
    .tag {
        display: inline-block;
        padding: 2px 8px;
        border-radius: 2px;
        font-size: 10px;
        font-weight: 600;
        letter-spacing: 1px;
        text-transform: uppercase;
        background-color: #ebf4ff;
        color: #1a2b4a !important;
        margin-right: 4px;
    }
</style>
""", unsafe_allow_html=True)

# RSS 뉴스 소스
RSS_FEEDS = {
    "Reuters Business": "https://feeds.reuters.com/reuters/businessNews",
    "Yahoo Finance": "https://finance.yahoo.com/news/rssindex",
    "Bloomberg Markets": "https://feeds.bloomberg.com/markets/news.rss",
    "CNBC Finance": "https://www.cnbc.com/id/10000664/device/rss/rss.html",
}

@st.cache_resource
def get_llm():
    return ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        temperature=0.3
    )

def fetch_news(feed_url, max_items=5):
    try:
        feed = feedparser.parse(feed_url)
        news = []
        for entry in feed.entries[:max_items]:
            news.append({
                "title": entry.get("title", "No title"),
                "link": entry.get("link", ""),
                "published": entry.get("published", ""),
                "summary": entry.get("summary", "")[:300]
            })
        return news
    except:
        return []

def summarize_news(llm, title, content):
    prompt = f"""
You are a financial analyst. Summarize the following news in 2-3 sentences in Korean.
Focus on: key facts, market impact, and investment implications.

Title: {title}
Content: {content}

Provide a concise Korean summary:
"""
    response = llm.invoke([HumanMessage(content=prompt)])
    return response.content

def analyze_sentiment(llm, news_list):
    titles = "\n".join([f"- {n['title']}" for n in news_list])
    prompt = f"""
You are a financial analyst. Based on these news headlines, provide:
1. Overall market sentiment (Bullish/Neutral/Bearish)
2. Key themes (2-3 bullet points in Korean)
3. Risk factors (1-2 bullet points in Korean)

Headlines:
{titles}

Respond in Korean:
"""
    response = llm.invoke([HumanMessage(content=prompt)])
    return response.content

# 상단 바
now = datetime.now().strftime("%Y.%m.%d  %H:%M")
st.markdown(f"""
<div class="top-bar">
    <div>
        <div class="top-bar-title">Finance News Intelligence Agent</div>
        <div class="top-bar-sub">Powered by Gemini 1.5 &nbsp;|&nbsp; Real-time Financial News Analysis</div>
    </div>
    <div class="top-bar-date">{now}</div>
</div>
""", unsafe_allow_html=True)

# 사이드바
with st.sidebar:
    st.markdown('<div style="padding:24px 20px 16px; border-bottom:1px solid #1e3a5f; margin-bottom:24px;"><div style="font-size:16px; font-weight:600; color:white;">News Agent</div><div style="font-size:10px; color:#4a6fa5; letter-spacing:2px; text-transform:uppercase;">Financial Intelligence</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="section-label">News Source</div>', unsafe_allow_html=True)
    selected_source = st.selectbox("", list(RSS_FEEDS.keys()), label_visibility="collapsed")

    st.markdown('<br>', unsafe_allow_html=True)
    st.markdown('<div class="section-label">Articles</div>', unsafe_allow_html=True)
    max_items = st.slider("", 3, 10, 5, label_visibility="collapsed")

    st.markdown('<br>', unsafe_allow_html=True)
    fetch_btn = st.button("Fetch & Analyze", use_container_width=True)

    st.markdown('<br><br>', unsafe_allow_html=True)
    st.markdown('<div class="section-label">System</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-size:11px; padding:0 4px; line-height:2;"><div>Model &nbsp;&nbsp; Gemini 1.5 Flash</div><div>Source &nbsp;&nbsp; RSS Feed</div><div>Agent &nbsp;&nbsp; LangChain</div></div>', unsafe_allow_html=True)

# 메인
if fetch_btn:
    llm = get_llm()

    with st.spinner("Fetching news..."):
        news_list = fetch_news(RSS_FEEDS[selected_source], max_items)

    if not news_list:
        st.error("Failed to fetch news. Please try another source.")
    else:
        # 시장 분석
        st.markdown("### Market Sentiment Analysis")
        with st.spinner("Analyzing market sentiment..."):
            sentiment = analyze_sentiment(llm, news_list)

        st.markdown(f"""
        <div class="news-card" style="border-left-color: #c9a84c;">
            <div class="news-meta">AI ANALYSIS &nbsp;|&nbsp; {selected_source} &nbsp;|&nbsp; {now}</div>
            <div class="news-summary">{sentiment}</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown(f"### News Articles — {selected_source}")

        # 뉴스 카드
        for i, news in enumerate(news_list):
            with st.spinner(f"Summarizing article {i+1}/{len(news_list)}..."):
                summary = summarize_news(llm, news['title'], news['summary'])

            st.markdown(f"""
            <div class="news-card">
                <div class="news-meta">{news['published']} &nbsp;|&nbsp; <span class="tag">Finance</span></div>
                <div class="news-title"><a href="{news['link']}" target="_blank" style="color:#1a2b4a; text-decoration:none;">{news['title']}</a></div>
                <div class="news-summary">{summary}</div>
            </div>
            """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div style="text-align:center; padding:80px 0; color:#a0aec0;">
        <div style="font-size:14px; font-weight:500; color:#4a5568; margin-bottom:8px;">Select a news source and click Fetch & Analyze</div>
        <div style="font-size:12px;">Real-time financial news summarization powered by AI</div>
    </div>
    """, unsafe_allow_html=True)