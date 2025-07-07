import os
import requests
import feedparser
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Load keys
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
CUSTOM_PROMPT = os.getenv("CUSTOM_PROMPT")

genai.configure(api_key=GEMINI_API_KEY)

# Keywords
KEYWORDS = [
    "Messi", "Ronaldo", "Mbappe", "Haaland", "Real Madrid", "Barcelona", "PSG",
    "Champions League", "Premier League", "World Cup", "La Liga"
]

# Get trending topics
def get_trending_topics():
    topics = []
    for keyword in KEYWORDS:
        url = f"https://news.google.com/rss/search?q={keyword}+football&hl=en-IN&gl=IN&ceid=IN:en"
        feed = feedparser.parse(url)
        if feed.entries:
            topics.append(feed.entries[0].title)
        if len(topics) >= 3:
            break
    return topics

# Generate blog using Gemini
def generate_blog(topic):
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content([CUSTOM_PROMPT, f"Write a blog on: {topic}"])
        return response.text
    except Exception as e:
        return f"Error generating blog for {topic}: {e}"

# Send to Telegram
def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }
    requests.post(url, data=data)

# Run the bot
def run_blog_bot():
    print("Running Football BlogBot...")
    topics = get_trending_topics()
    for topic in topics:
        blog = generate_blog(topic)
        send_to_telegram(f"Topic: {topic}\n\n{blog}")
