from flask import Flask
import threading
import schedule
import time
from blogbot import run_blog_bot

app = Flask(__name__)

@app.route('/')
def home():
    return "Football BlogBot is running on Render!"

# ✅ Function to run the scheduler in a thread
def run_scheduler():
    schedule.every().day.at("06:30").do(run_blog_bot)  # IST 6:30 AM = UTC 1:00 AM

    while True:
        schedule.run_pending()
        time.sleep(30)

if __name__ == "__main__":
    # Start the scheduler in a background thread
    threading.Thread(target=run_scheduler).start()

    # Start Flask app to keep port open (Render needs this)
    app.run(host="0.0.0.0", port=10000)
