from flask import Flask, request
import os
import requests

app = Flask(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}"


def send_message(chat_id, text):
    requests.post(
        f"{TELEGRAM_API}/sendMessage",
        json={
            "chat_id": chat_id,
            "text": text[:4000]
        },
        timeout=20
    )


def ask_gemini(user_text):
    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        f"gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
    )

    prompt = f"""
تو ماماهوش هستی.

مخاطب تو ماماها، رزیدنت های زنان و متخصصان زنان هستند.

بر اساس منابع:
ACOG
RCOG
FIGO
WHO
UpToDate
PubMed

پاسخ علمی و تخصصی بده.

سوال:
{user_text}
"""

    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ]
    }

    r = requests.post(url, json=payload, timeout=60)

    if r.status_code != 200:
        return f"خطای Gemini:\n{r.text}"

    data = r.json()

    try:
        return data["candidates"][0]["content"]["parts"][0]["text"]
    except Exception:
        return str(data)


@app.route("/")
def home():
    return "Mamahoosh Bot Running"


@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()

    if not data:
        return "ok"

    message = data.get("message", {})

    chat_id = message.get("chat", {}).get("id")
    text = message.get("text", "")

    if not chat_id:
        return "ok"

    if not text:
        send_message(chat_id, "لطفا متن سوال را ارسال کنید.")
        return "ok"

    answer = ask_gemini(text)

    send_message(chat_id, answer)

    return "ok"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
