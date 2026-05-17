"""
llm_client.py — LLM wrapper using Groq (free tier)

Groq gives free access to llama-3.3-70b-versatile, which is more than
sufficient for Text-to-SQL tasks.

Get a free API key at: https://console.groq.com
"""

import os
import json
import logging
import re

from dotenv import load_dotenv
import requests

logger = logging.getLogger(__name__)

# ── Config ───────────────────────────────────────────────────────────────────
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise RuntimeError(
        "GROQ_API_KEY is required. Set it in your environment or in a .env file."
    )
GROQ_MODEL = "llama-3.3-70b-versatile"
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"


def call_llm(prompt: str, temperature: float = 0.0, max_tokens: int = 1024) -> str:
    """
    Call the Groq LLM and return the text response.
    Raises RuntimeError on failure.
    """
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": GROQ_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": temperature,
        "max_tokens": max_tokens,
    }

    try:
        response = requests.post(GROQ_URL, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"].strip()
    except requests.RequestException as e:
        logger.error(f"LLM call failed: {e}")
        raise RuntimeError(f"LLM unavailable: {e}")


def call_llm_json(prompt: str) -> dict:
    """
    Call LLM and parse JSON from the response.
    Strips markdown fences if present.
    """
    raw = call_llm(prompt, temperature=0.0)
    # Strip ```json ... ``` if model adds it despite instructions
    clean = re.sub(r"```(?:json)?\s*", "", raw).replace("```", "").strip()
    try:
        return json.loads(clean)
    except json.JSONDecodeError as e:
        logger.error(f"JSON parse failed. Raw:\n{raw}\nError: {e}")
        raise ValueError(f"LLM returned invalid JSON: {e}\nRaw: {raw}")
