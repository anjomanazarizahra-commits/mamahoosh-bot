import os
import requests
from flask import Flask, request

app = Flask(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}"

def send_message(chat_id, text):
    requests.post(f"{TELEGRAM_API}/sendMessage", json={
        "chat_id": chat_id,
        "text": text
    })

def ask_ai(user_text):
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    system_prompt = """
    تو یک دستیار تخصصی مامایی و زنان هستی.
    پاسخ‌ها باید:
    - علمی و مبتنی بر ACOG / UpToDate باشند
    - برای بیماران قابل فهم باشند
    - علائم خطر را هشدار بدهی
    - تشخیص قطعی ندهی، فقط راهنمایی پزشکی بدهی
    """

    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_text}
        ]
    }

    res = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers=headers,
        json=payload
    )

    return res.json()["choices"][0]["message"]["content"]

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()

    message = data["message"]
    chat_id = message["chat"]["id"]
    text = message.get("text", "")

    reply = ask_ai(text)

    send_message(chat_id, reply)

    return "ok" 

