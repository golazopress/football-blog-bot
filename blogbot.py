import os
import requests
import feedparser
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Load credentials from .env
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-pro")

# Blog generation prompt template
PROMPT_TEMPLATE = """
Write a detailed blog post from a human perspective on the following football news topic. Include emotional and expert-level insight, match stats, team context, and possible implications. Make it feel like a personal blog written by a fan who understands the game deeply.

Topic: {topic}
"""

def fetch_trending_football_topics():
    rss_url = "https://news.google.com/rss/search?q=football&hl=en-IN&gl=IN&ceid=IN:en"
    feed = feedparser.parse(rss_url)
    top_topics = [entry.title for entry in
