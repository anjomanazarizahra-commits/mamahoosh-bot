def ask_ai(text):
    try:
        r = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENAI_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "gpt-3.5-turbo",
                "messages": [
                    {"role": "system", "content": "تو دستیار مامایی هستی"},
                    {"role": "user", "content": text}
                ]
            },
            timeout=20
        )

        data = r.json()

        # 👇 این خط جلوی کرش رو می‌گیره
        if "choices" not in data:
            return f"API Error: {data}"

        return data["choices"][0]["message"]["content"]

    except Exception as e:
        return f"خطای سرور: {str(e)}"
