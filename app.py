def ask_ai(text):
    try:
        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json"
        }

        data = {
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": "تو یک دستیار مامایی هستی"},
                {"role": "user", "content": text}
            ]
        }

        r = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=20
        )

        res = r.json()

        return res["choices"][0]["message"]["content"]

    except Exception as e:
        return "مشکل موقت در سرور ❌"
