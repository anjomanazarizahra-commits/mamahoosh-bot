from flask import Flask, request
import os
import requests

app = Flask(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN")

def send(chat_id, text):
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        json={"chat_id": chat_id, "text": text}
    )

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()

    msg = data.get("message", {})
    chat_id = msg.get("chat", {}).get("id")
    text = msg.get("text", "")

    # 👇 جواب ساده و قطعی (بدون AI که خراب بشه)
    if "سلام" in text:
        reply = "سلام عزیزم 🌸"
    else:
        reply = "پیامت دریافت شد ✅"

    send(chat_id, reply)

    return "ok"
