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


def ask_ai(user_text):
    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "deepseek/deepseek-chat-v3-0324:free",
        "messages": [
            {
                "role": "system",
                "content": """تو ماماهوش هستی.
مخاطب تو ماماها، رزیدنت‌های زنان و متخصصان زنان هستند.
بر اساس ACOG، RCOG، FIGO، WHO، UpToDate و PubMed پاسخ دقیق و علمی بده.
اگر از پاسخ مطمئن نبودی، صادقانه اعلام کن."""
            },
            {
                "role": "user",
                "content": user_text
            }
        ]
    }

    r = requests.post(url, headers=headers, json=payload, timeout=60)

    if r.status_code != 200:
        return f"خطای OpenRouter:\n{r.text}"

    data = r.json()

    try:
        return data["choices"][0]["message"]["content"]
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
