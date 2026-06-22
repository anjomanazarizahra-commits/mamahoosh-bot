import os
import requests
from flask import Flask, request

app = Flask(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}"

def send_message(chat_id, text):
    requests.post(f"{TELEGRAM_API}/sendMessage", json={
        "chat_id": chat_id,
        "text": text
    })

@app.route("/", methods=["GET"])
def home():
    return "ماماهوش آنلاین شد 👶💜"

# 👇 این همون چیزیه که نداشتی!!!
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()

    if not data:
        return "no data", 200

    message = data.get("message")
    if not message:
        return "no message", 200

    chat_id = message["chat"]["id"]
    text = message.get("text", "")

    if "سلام" in text:
        reply = "سلام عزیزم 👶💜 من ماماهوش هستم"
    else:
        reply = "پیامت رسید 💜 به زودی هوشمندتر میشم"

    send_message(chat_id, reply)

    return "ok", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

