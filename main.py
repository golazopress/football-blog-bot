from flask import Flask
import threading
import time
import datetime
import subprocess

app = Flask(__name__)

def run_bot_daily():
    while True:
        now = datetime.datetime.utcnow()
        if now.hour == 1 and now.minute == 0:  # 6:30 AM IST = 1:00 AM UTC
            print("Running blogbot.py at 6:30 AM IST...")
            subprocess.call(["python", "blogbot.py"])
            time.sleep(60)  # Avoid multiple runs in one minute
        time.sleep(20)  # Check every 20 seconds

@app.route('/')
def home():
    return "Football Blog Bot is running."

if __name__ == '__main__':
    threading.Thread(target=run_bot_daily, daemon=True).start()
    app.run(host='0.0.0.0', port=10000)
