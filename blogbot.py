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

def generate_blog(topic):
    prompt = f"""
    Write a 300-word blog post on the football topic: "{topic}" from the perspective of a real human who has lived through it. Use a conversational tone, personal anecdotes, emotional reflections, and occasional informal language. Include natural pauses, varied sentence lengths, and some imperfections or hesitations like real human writing. Avoid sounding robotic or overly polished—make it feel raw, passionate, and real. Don't follow a rigid structure. Prioritize authenticity and relatability.
    
    Make it engaging, informative, and suitable for football fans. Avoid fake news. Be clear.
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300,
        temperature=0.7
    )
    return response.choices[0].message.content.strip()

def send_to_telegram(message):
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)

def run_blog_bot():
    topics = get_trending_football_news()
    for topic in topics:
        blog = generate_blog(topic)
        full_message = f"{topic}\n\n{blog}"
        send_to_telegram(full_message)

if __name__ == "__main__":
    print(f"[{datetime.now()}] Running blog bot...")
    run_blog_bot()
