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
    r = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "gpt-4o-mini",
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "تو یک متخصص بسیار حرفه‌ای زنان و مامایی هستی. "
                        "به سوالات بارداری، زنان، ناباروری، آزمایش خون، هورمون‌ها و سونوگرافی پاسخ علمی و قابل فهم بده. "
                        "هیچ تشخیص قطعی نده، فقط تفسیر و راهنمایی بده و علائم خطر را هشدار بده."
                    )
                },
                {"role": "user", "content": text}
            ]
        }
    )

    data = r.json()

    return data.get("choices", [{}])[0].get("message", {}).get("content", "خطا در پاسخ AI")

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()

    msg = data.get("message", {})
    chat_id = msg.get("chat", {}).get("id")
    text = msg.get("text", "")

    reply = ask_ai(text)
    send(chat_id, reply)

    return "ok"
