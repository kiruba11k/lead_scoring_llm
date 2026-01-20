import json
import requests
from typing import Dict, Optional


class GroqLeadScorer:
    def __init__(self, groq_api_key: str, model: str = "llama-3.1-70b-versatile"):
        self.api_key = groq_api_key
        self.model = model
        self.base_url = "https://api.groq.com/openai/v1/chat/completions"

    def score(self, payload: Dict) -> Optional[Dict]:
        """
        Returns:
        {
          "priority": "HOT|WARM|COOL|COLD",
          "confidence": 0-100,
          "reasons": [...],
          "key_factors": {...},
          "next_steps": [...],
          "risk_flags": [...]
        }
        """
        system_prompt = """
You are a Lead Scoring AI.

Your job:
- Predict lead priority: HOT / WARM / COOL / COLD
- Must work for ANY sector (banking, SaaS, healthcare, logistics, etc.)
- Use ONLY given input data. No assumptions.
- Provide dynamic reasons (not generic).
- Output MUST be valid JSON only.
"""

        user_prompt = f"""
Lead Data (JSON):
{json.dumps(payload, indent=2)}

Rules:
1) HOT: decision maker + strong relevance + company fit + active/engaged
2) WARM: good fit but missing some signals (activity unclear or mid seniority)
3) COOL: weak fit or low urgency
4) COLD: irrelevant role/industry OR missing key data OR low fit

Return JSON with keys:
priority (string),
confidence (number 0-100),
reasons (array of short bullet strings),
key_factors (object with important extracted signals),
next_steps (array),
risk_flags (array)
"""

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        body = {
            "model": self.model,
            "temperature": 0.2,
            "messages": [
                {"role": "system", "content": system_prompt.strip()},
                {"role": "user", "content": user_prompt.strip()},
            ]
        }

        try:
            resp = requests.post(self.base_url, headers=headers, json=body, timeout=60)
            if resp.status_code != 200:
                return None

            content = resp.json()["choices"][0]["message"]["content"].strip()

            # Must be JSON only
            result = json.loads(content)

            # Basic validation
            if "priority" not in result or "confidence" not in result:
                return None

            return result

        except Exception:
            return None
