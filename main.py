from flask import Flask
import threading
import schedule
import time
import os
from blogbot import run_blog_bot

app = Flask(__name__)

@app.route('/')
def home():
    return "Football BlogBot is running!"

def run_scheduler():
    schedule.every().day.at("01:00").do(run_blog_bot)  # 6:30 AM IST = 1:00 AM UTC
    while True:
        schedule.run_pending()
        time.sleep(30)

if __name__ == "__main__":
    threading.Thread(target=run_scheduler, daemon=True).start()

    # ✅ Bind to Render's required port
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
