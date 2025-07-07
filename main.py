from flask import Flask
import schedule
import time
import threading
from blogbot import run_blog_bot

app = Flask(__name__)

@app.route('/')
def home():
    return "Football BlogBot is Running!"

def job():
    run_blog_bot()

# Schedule daily at 6:30 AM IST
schedule.every().day.at("01:00").do(job)  # 6:30 AM IST = 1:00 UTC

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(60)

threading.Thread(target=run_scheduler).start()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
