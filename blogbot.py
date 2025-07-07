# blogbot.py

import os
import requests
import feedparser
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Configure Gemini API
genai.configure(api_key=GOOGLE_API_KEY)

# Short football-related keywords to find trending topics
KEYWORDS = [
    "Messi", "Ronaldo", "Mbappe", "Haaland", "Barcelona", "Real Madrid",
    "Liverpool", "Arsenal", "Manchester United", "PSG", "Champions League",
    "Premier League", "La Liga", "Bundesliga", "Cristiano", "Argentina",
    "Portugal", "Yamal", "Van Dijk", "World Cup", "UEFA", "Controversy"
]

# Fetch trending football news topics using Google News RSS
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

# Generate blog content using Gemini
def generate_blog(topic):
    try:
        model = genai.GenerativeModel("gemini-pro")
        prompt = f"Write an engaging, detailed football blog about this topic from a human perspective:\n\n{topic}"
        response = model.generate_content(prompt)
        return response.text.strip() if response.text else "Blog generation failed. Empty response."
    except Exception as e:
        return f"Error generating blog for {topic}: {str(e)}"

# Send message to Telegram
def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }
    requests.post(url, data=data)

# Main bot runner
def run_blog_bot():
    print("Running Football BlogBot...")
    topics = get_trending_topics()
    for topic in topics:
        blog = generate_blog(topic)
        full_message = f"📝 Topic: {topic}\n\n{blog}"
        send_to_telegram(full_message)
