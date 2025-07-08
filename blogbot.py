import os
import feedparser
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

RSS_FEED_URL = "https://news.google.com/rss/search?q=football&hl=en-IN&gl=IN&ceid=IN:en"

def get_trending_topics(max_articles=5):
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
        message = f" You are a human football blogger who has lived and breathed the sport — not an AI. Your job is to write a personal, natural, emotional blog post based on the topic:------------------------------------------------- {topic} ----------------------------------------------------- Write as if you're talking to real football fans. Use a raw, human tone , natural pauses, personal opinions, and some mild humor where appropriate.Don’t sound robotic or overly polished — instead, mix short and long sentences, add slight hesitations like honestly or I mean, come on, and let your emotions and passion for the game show.Make it feel like someone who just watched the game or read the news and ran straight to blog their thoughts — not a scripted news article.Use at least 2 personal anecdotes or emotional reflections if the topic allows.Avoid filler or repetition — just keep it genuine, relatable, and flowing.Insert light humor but don’t force jokes — it should feel natural.Write a clickable, SEO-optimized blog title that includes relevant keywords, but don’t make it funny — it should sound professional and engaging.Ensure the blog is SEO friendly use headings/subheadings, include important football keywords naturally, and keep paragraphs short and readable.IMPORTANT: Do NOT include any AI-style phrases like As an AI language model, In conclusion, Here a summary — you are NOT an AI, you are a real football fan writing from the heart.Limit the blog to about 500–600 words. Title should be within 8–12 words."
        print(" Sending to Telegram:", topic)
        send_to_telegram(message)

    print(" Done at", datetime.now())
