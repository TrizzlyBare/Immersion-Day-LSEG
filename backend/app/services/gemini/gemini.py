# app/services/gemini_client.py
import httpx
import json
from app.core.config import settings

async def call_gemini(prompt: str, max_tokens: int = 800, temperature: float = 0.7):
    url = f"{settings.GEMINI_BASE_URL}/chat/completions"
    headers = {
        "Authorization": f"Bearer {settings.GEMINI_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": settings.GEMINI_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens,
        "temperature": temperature,
    }

    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.post(url, headers=headers, json=payload)
        r.raise_for_status()
        data = r.json()

    try:
        return data["choices"][0]["message"]["content"]
    except Exception:
        return json.dumps(data)