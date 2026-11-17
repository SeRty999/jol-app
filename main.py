import os, time, requests

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
AI_KEY = os.environ["OPENAI_API_KEY"]
API = f"https://api.telegram.org/bot{TOKEN}"

offset = 0
while True:
    try:
        r = requests.get(f"{API}/getUpdates", params={"offset": offset, "timeout": 30}, timeout=40)
        for upd in r.json().get("result", []):
            offset = upd["update_id"] + 1
            msg = upd.get("message")
            if not msg or "text" not in msg:
                continue
            chat_id = msg["chat"]["id"]
            text = msg["text"]
            ai = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={"Authorization": f"Bearer {AI_KEY}"},
                json={
                    "model": "llama-3.1-8b-instant",
                    "messages": [
                        {"role": "system", "content": "Ты — JoL, дружелюбный ассистент. Отвечай кратко и по делу."},
                        {"role": "user", "content": text},
                    ],
                },
                timeout=60,
            )
            answer = ai.json()["choices"][0]["message"]["content"]
            requests.post(f"{API}/sendMessage", json={"chat_id": chat_id, "text": answer}, timeout=30)
    except Exception as e:
        print("error:", e)
        time.sleep(5)
