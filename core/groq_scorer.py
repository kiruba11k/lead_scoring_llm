import requests
import json
import os

class GroqLeadScorer:
    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError("Groq API key missing")
        self.api_key = api_key
        self.url = "https://api.groq.com/openai/v1/chat/completions"
        self.model = "llama-3.1-8b-instant"

    def score(self, prospect: dict) -> dict:
        """
        Returns:
        {
          priority: HOT|WARM|COOL|COLD,
          confidence: float (0-100),
          reasons: [str, str, ...]
        }
        """

        prompt = f"""
You are a B2B lead intelligence system.

Classify the prospect into one category:
HOT, WARM, COOL, or COLD.

Rules:
- HOT: senior decision-maker + strong domain fit + large org or revenue
- WARM: senior or mid-senior + good fit
- COOL: senior but weak fit or low activity
- COLD: junior or irrelevant

Prospect Data (may have missing fields):
{json.dumps(prospect, indent=2)}

Respond ONLY in valid JSON:
{{
  "priority": "...",
  "confidence": 0-100,
  "reasons": ["...", "..."]
}}
"""

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "You are an expert sales intelligence analyst."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.2
        }

        resp = requests.post(self.url, headers=headers, json=payload, timeout=60)

        if resp.status_code != 200:
            raise RuntimeError(f"Groq API error: {resp.text}")

        text = resp.json()["choices"][0]["message"]["content"]

        try:
            return json.loads(text)
        except Exception:
            raise RuntimeError(f"Invalid JSON from LLM:\n{text}")
