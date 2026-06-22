import os
import requests
from flask import Flask, request

app = Flask(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}"

def send_message(chat_id, text):
    url = f"{TELEGRAM_API}/sendMessage"
    data = {"chat_id": chat_id, "text": text}
    requests.post(url, data=data)

@app.route("/", methods=["GET"])
def home():
    return "ماماهوش آنلاین شد 👶💜"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()

    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")

        # پاسخ ساده اولیه ماماهوش
        if "سلام" in text:
            reply = "سلام عزیزم 👶💜 من ماماهوش هستم، چطور کمکت کنم؟"
        else:
            reply = "پیامت رو گرفتم 💜 به زودی هوشمندتر میشم"

        send_message(chat_id, reply)

    return "ok", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
