# GIMBOT OS2 — Automated Football Blog Bot using OpenRouter + Telegram + Google News

import os
import requests
import feedparser
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()  # Loads variables from .env or Render's environment settings

# ✅ Fetch top 3 trending football topics from Google News RSS
def get_trending_football_topics():
    query_keywords = [
        "football", "soccer", "Barcelona", "Real Madrid", "Cristiano Ronaldo", "Messi",
        "Mbappe", "Haaland", "Premier League", "Champions League", "Euro 2024",
        "Liverpool", "Manchester United", "Argentina", "Portugal", "France",
        "La Liga", "Serie A", "Bundesliga", "transfer news", "fixtures", "controversy"
    ]

    topic_results = []

    for keyword in query_keywords:
        url = f"https://news.google.com/rss/search?q={keyword}+when:1d&hl=en-IN&gl=IN&ceid=IN:en"
        feed = feedparser.parse(url)

        for entry in feed.entries:
            topic_results.append(entry.title)

        if len(topic_results) >= 3:
            break

    return topic_results[:3]

# ✅ Generate blog content using OpenRouter with human-style writing prompt
def generate_blog(topic):
    prompt = f"""
    Write a football blog post (around 200 words) about this topic: "{topic}"

    Write it from the perspective of a real human who has lived through it.
    Use a conversational tone, personal anecdotes, emotional reflections, and occasional informal language.
    Include natural pauses, varied sentence lengths, and some imperfections or hesitations like real human writing.
    Avoid sounding robotic or overly polished—make it feel raw, passionate, and real.
    Don't follow a rigid structure. Prioritize authenticity and relatability.
    """

    headers = {
        "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
    result = response.json()
    return result["choices"][0]["message"]["content"].strip()
