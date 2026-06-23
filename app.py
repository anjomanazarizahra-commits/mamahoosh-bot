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
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={os.environ.get('GEMINI_API_KEY')}"

        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": f"""
تو یک متخصص زنان و مامایی با تجربه هستی.
به سوالات بارداری، ناباروری، آزمایش‌ها، سونوگرافی و بیماری‌های زنان پاسخ علمی و قابل فهم بده.
اگر علائم خطر وجود داشت هشدار بده
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
