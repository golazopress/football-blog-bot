import os
import requests
from pytrends.request import TrendReq
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("7346083970:AAEpBsY0jY11ApZBHiOONeiLPDYHM7yyNTE")
CHAT_ID = os.getenv("5044388916")
OPENROUTER_API_KEY = os.getenv("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")
CUSTOM_PROMPT = os.getenv("CUSTOM_PROMPT", "Write a 600-word blog post on the football topic: {topic} from the perspective of a real human who has lived through it. Use a conversational tone, personal anecdotes, emotional reflections, and occasional informal language. Include natural pauses, varied sentence lengths, and some imperfections or hesitations like real human writing. Avoid sounding robotic or overly polished—make it feel raw, passionate, and real. Don't follow a rigid structure. Prioritize authenticity and relatability.")

def get_trending_football_topics():
    pytrends = TrendReq(hl='en-US', tz=360)
    pytrends.build_payload(kw_list=["football"], cat=0, timeframe='now 1-d')
    try:
        df = pytrends.related_queries()
        top_related = df["football"]["top"]
        if top_related is not None:
            top_topics = [row["query"] for _, row in top_related.head(3).iterrows()]
        else:
            raise Exception("No related topics")
    except:
        top_topics = ["Latest Football News", "Football Transfer Rumors", "Match Highlights"]
    return top_topics

def generate_blog(topic):
    prompt = CUSTOM_PROMPT.replace("{topic}", topic)
    headers = {
        "Authorization": f"Bearer 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",
        "Content-Type": "application/json"
    }
    data = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}]
    }
    try:
        res = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
        res.raise_for_status()
        return res.json()['choices'][0]['message']['content']
    except Exception as e:
        return f"Blog generation failed for topic: {topic}\nError: {e}"

def send_telegram_message(text):
    url = f"https://api.telegram.org/bot7346083970:AAEpBsY0jY11ApZBHiOONeiLPDYHM7yyNTE/sendMessage"
    data = {"chat_id": 5044388916, "text": text}
    requests.post(url, data=data)

if __name__ == "__main__":
    topics = get_trending_football_topics()
    for topic in topics:
        blog = generate_blog(topic)
        send_telegram_message(f"{topic}\n\n{blog}")
