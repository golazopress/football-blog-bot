import os
import requests
import feedparser
import google.generativeai as genai
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

# Load environment variables
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Configure Gemini API
if not GOOGLE_API_KEY:
    raise ValueError("Missing GOOGLE_API_KEY in environment variables.")

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel(model_name="gemini-pro")

# Fetch top football topics from Google News RSS
def get_top_football_topics():
    url = "https://news.google.com/rss/search?q=football&hl=en-IN&gl=IN&ceid=IN:en"
    feed = feedparser.parse(url)
    topics = []
    for entry in feed.entries[:3]:
        topics.append({"title": entry.title, "link": entry.link})
    return topics

# Generate blog using Gemini API
def generate_blog(topic):
    try:
        prompt = f"Write an engaging, detailed football blog about this topic:\n\n{topic}"
        response = model.generate_content(prompt)
        return response.text.strip() if response.text else "Blog generation failed. Empty response."
    except Exception as e:
        return f"Error generating blog for {topic}: {str(e)}"

# Send blog to Telegram
def send_to_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "HTML"
    }
    try:
        response = requests.post(url, data=payload)
        print(f"Telegram Response {response.status_code}: {response.text}")
    except Exception as e:
        print(f"Telegram Error: {str(e)}")

# Main runner
def run_blog_bot():
    print("\n\nRunning Football BlogBot...")
    topics = get_top_football_topics()
    for topic in topics:
        blog = generate_blog(topic["title"])
        message = f"\ud83d\udccd <b>Topic:</b> {topic['title']}\n{topic['link']}\n\n<pre>{blog}</pre>"
        send_to_telegram(message)

if __name__ == "__main__":
    run_blog_bot()
