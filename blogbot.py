# blogbot.py

import os
import requests
import feedparser
from dotenv import load_dotenv

load_dotenv()

# Load environment variables
TELEGRAM_BOT_TOKEN = os.getenv("7346083970:AAEpBsY0jY11ApZBHiOONeiLPDYHM7yyNTE")
TELEGRAM_CHAT_ID = os.getenv("5044388916")
OPENROUTER_API_KEY = os.getenv("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")
CUSTOM_PROMPT = os.getenv("from the perspective of a real human who has lived through it.
    Use a conversational tone, personal anecdotes, emotional reflections, and occasional informal language.
    Include natural pauses, varied sentence lengths, and some imperfections or hesitations like real human writing.
    Avoid sounding robotic or overly polished—make it feel raw, passionate, and real.
    Don't follow a rigid structure. Prioritize authenticity and relatability")

# Use short football-related keywords
KEYWORDS = [
    "Messi", "Ronaldo", "Mbappe", "Haaland", "Barcelona", "Real Madrid", "Liverpool",
    "Arsenal", "Manchester United", "PSG", "Champions League", "Premier League",
    "La Liga", "Bundesliga", "Cristiano", "Argentina", "Portugal", "Yamal", "Van Dijk",
    "World Cup", "UEFA", "Barcelona fixture", "Real Madrid fixture", "Controversy"
]

def get_trending_topics():
    topics = []
    for keyword in KEYWORDS:
        url = f"https://news.google.com/rss/search?q={keyword}+football&hl=en-IN&gl=IN&ceid=IN:en"
        feed = feedparser.parse(url)
        if feed.entries:
            entry = feed.entries[0]
            topics.append(entry.title)
        if len(topics) >= 3:
            break
    return topics

def generate_blog(topic):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "openrouter/auto",
        "messages": [
            {"role": "system", "content": CUSTOM_PROMPT},
            {"role": "user", "content": f"Write a blog about: {topic}"}
        ]
    }
    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
    
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        return f"Error generating blog for {topic}: {response.text}"

def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }
    requests.post(url, data=data)

def run_blog_bot():
    print(" Running Football BlogBot...")
    topics = get_trending_topics()
    for topic in topics:
        blog = generate_blog(topic)
        send_to_telegram(f" Topic: {topic}\n\n{blog}")
