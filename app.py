from flask import Flask, request
import os
import requests

app = Flask(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

def send(chat_id, text):
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        json={"chat_id": chat_id, "text": text}
    )

def ask_ai(text):
    try:
        r = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENAI_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "gpt-4o-mini",
                "messages": [
                    {"role": "system", "content": "تو دستیار مامایی هستی"},
                    {"role": "user", "content": text}
                ]
            },
            timeout=20
        )

        data = r.json()

        return data.get("choices", [{}])[0].get("message", {}).get("content", "خطا در AI")

    except:
        return "مشکل در سرور ❌"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()

    msg = data.get("message", {})
    chat_id = msg.get("chat", {}).get("id")
    text = msg.get("text", "")

    reply = ask_ai(text)
    send(chat_id, reply)

    return "ok"
