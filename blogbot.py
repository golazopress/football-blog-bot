import os
import requests
import feedparser
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

if not GEMINI_API_KEY:
    print("GEMINI_API_KEY not found. Check your .env file.")
    exit(1)

# Configure Gemini with the API key
try:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel("models/gemini-pro")
except Exception as e:
    print(f"Gemini configuration failed: {e}")
    exit(1)

RSS_FEED_URL = "https://news.google.com/rss/search?q=football&hl=en-IN&gl=IN&ceid=IN:en"

def get_top_trending_topics(limit=3):
    feed = feedparser.parse(RSS_FEED_URL)
    return feed.entries[:limit]

def generate_blog(title, summary=""):
    prompt = (
        f"Write a 300–400 word football blog post on the topic:\n\n"
        f"{title}\n\n"
        f"Include detailed analysis, background context, and ensure the tone is like a real human football blogger. Avoid repetition and be informative."
    )
    try:
        response = model.generate_content(prompt)
        return response.text.strip() if response and hasattr(response, 'text') else "Blog content generation failed."
    except Exception as e:
        return f"Gemini API error: {e}"

def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    try:
        res = requests.post(url, json=payload)
        if res.status_code != 200:
            print(f"Telegram Error {res.status_code}: {res.text}")
    except Exception as e:
        print(f"Telegram send failed: {e}")

def run_blog_bot():
    print("Running Football Blog Bot using Gemini API...")
    topics = get_top_trending_topics()

    if not topics:
        send_to_telegram("No trending football topics found.")
        return

    for entry in topics:
        title = entry.title
        link = entry.link
        summary = entry.get("summary", "")

        send_to_telegram(f"Topic: {title}")

        blog = generate_blog(title, summary)

        message = f"<b>{title}</b>\n\n<pre>{blog}</pre>\n\nLink: <a href='{link}'>Read more</a>"

        if len(message) > 4096:
            message = message[:4000] + "\n\n...truncated"

        send_to_telegram(message)
