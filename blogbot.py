import os
import feedparser
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

RSS_FEED_URL = "https://news.google.com/rss/search?q=football&hl=en-IN&gl=IN&ceid=IN:en"

def get_trending_topics(max_articles=3):
    feed = feedparser.parse(RSS_FEED_URL)
    entries = feed.entries[:max_articles]
    return [entry.title + " - " + entry.source.title for entry in entries]

def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    response = requests.post(url, data=data)
    return response

def run_blog_bot():
    print("🔍 Fetching trending topics...")
    topics = get_trending_topics()

    for topic in topics:
        message = f" Topic: {topic}"
        print(" Sending to Telegram:", topic)
        send_to_telegram(message)

    print(" Done at", datetime.now())
