from flask import Flask, request
import os
import requests

app = Flask(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

TELEGRAM_API = f"https://api.telegram.org/bot{BOT_TOKEN}"

# ---------------------------
# ارسال پیام به تلگرام
# ---------------------------
def send_message(chat_id, text):
    try:
        requests.post(
            f"{TELEGRAM_API}/sendMessage",
            json={
                "chat_id": chat_id,
                "text": text
            },
            timeout=10
        )
    except:
        pass


# ---------------------------
# گرفتن جواب از AI
# ---------------------------
def ask_ai(user_text):
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
                    {
                        "role": "system",
                        "content": (
                            "تو یک متخصص حرفه‌ای زنان و مامایی هستی. "
                            "به سوالات بارداری، ناباروری، هورمون‌ها، آزمایش‌ها و سونوگرافی پاسخ علمی و قابل فهم بده. "
                            "هیچ تشخیص قطعی نده. فقط تفسیر و راهنمایی بده و علائم خطر را هشدار بده."
                        )
                    },
                    {"role": "user", "content": user_text}
                ]
            },
            timeout=20
        )

        data = r.json()

        # اگر خطا از OpenAI آمد
        if "error" in data:
            return "خطا در AI: " + data["error"].get("message", "unknown error")

        return data.get("choices", [{}])[0].get("message", {}).get("content", "پاسخی دریافت نشد")

    except Exception as e:
        return f"خطای سرور: {str(e)}"


# ---------------------------
# webhook تلگرام
# ---------------------------
@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        data = request.get_json()

        msg = data.get("message", {})
        chat_id = msg.get("chat", {}).get("id")
        text = msg.get("text", "")

        if not chat_id:
            return "no chat"

        reply = ask_ai(text)
        send_message(chat_id, reply)

        return "ok"

    except:
        return "error"


# ---------------------------
# تست سرور
# ---------------------------
@app.route("/")
def home():
    return "Bot is running"
