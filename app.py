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
                {"role": "system", "content": "تو دستیار مامایی هستی"},
                {"role": "user", "content": text}
            ]
        }
    )

    data = r.json()

    return data.get("choices", [{}])[0].get("message", {}).get("content", "خطا در AI")
