import os
import openai
import feedparser
from datetime import datetime
from dotenv import load_dotenv
from telegram import Bot

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("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")
TELEGRAM_BOT_TOKEN = os.getenv("7346083970:AAEpBsY0jY11ApZBHiOONeiLPDYHM7yyNTE")
TELEGRAM_CHAT_ID = os.getenv("5044388916")

def get_trending_football_news():
    url = "https://news.google.com/rss/search?q=football"
    feed = feedparser.parse(url)
    headlines = [entry.title for entry in feed.entries[:3]]
    return headlines

import requests

import requests

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
