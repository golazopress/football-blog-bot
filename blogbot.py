import os
import requests
import feedparser
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

# Load environment variables
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
CUSTOM_PROMPT = os.getenv("CUSTOM_PROMPT", "Write an engaging football blog post about the topic.")

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-pro")

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
    try:
        prompt = f"{CUSTOM_PROMPT}\n\nTopic: {topic}"
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating blog for {topic}: {str(e)}"

def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }
    requests.post(url, data=data)

def run_blog_bot():
    print("Running Football BlogBot...")
    topics = get_trending_topics()
    for topic in topics:
        blog = generate_blog(topic)
        send_to_telegram(f"Topic: {topic}\n\n{blog}")
