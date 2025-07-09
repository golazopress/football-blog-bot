from flask import Flask
import threading
import schedule
import time
from blogbot import run_blog_bot
from bot_handler import main as telegram_main  # Import from the new bot_handler.py

app = Flask(__name__)

@app.route('/')
def home():
    return "Football BlogBot is Running!"

def job():
    run_blog_bot()

# Schedule for 6:30 AM and 6:30 PM IST (i.e., 01:00 & 13:00 UTC)
schedule.every().day.at("01:00").do(job)
schedule.every().day.at("13:00").do(job)

def run_scheduler():
    run_blog_bot()
    while True:
        schedule.run_pending()
        time.sleep(60)

# Start everything
if __name__ == '__main__':
    threading.Thread(target=run_scheduler).start()
    threading.Thread(target=telegram_main).start()
    app.run(host='0.0.0.0', port=10000)
