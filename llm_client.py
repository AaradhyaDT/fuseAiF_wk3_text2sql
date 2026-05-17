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

import time

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


CACHE_FILE = "logs/llm_cache.json"


def get_cached_response(prompt: str, temperature: float, max_tokens: int) -> str:
    """Retrieve response from cache if exists."""
    key = f"{prompt}_{temperature}_{max_tokens}"
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                cache = json.load(f)
                return cache.get(key)
        except Exception:
            pass
    return None


def save_to_cache(prompt: str, temperature: float, max_tokens: int, response: str):
    """Save response to cache."""
    key = f"{prompt}_{temperature}_{max_tokens}"
    cache = {}
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                cache = json.load(f)
        except Exception:
            pass
    cache[key] = response
    try:
        os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(cache, f, indent=2)
    except Exception:
        pass


def call_llm(prompt: str, temperature: float = 0.0, max_tokens: int = 1024) -> str:
    """
    Call the Groq LLM and return the text response.
    Checks the local file-based cache first to respect rate limits.
    Includes a multi-model fallback: tries llama-3.3-70b-versatile first,
    and falls back to llama-3.1-8b-instant if 429 with long cooldown is encountered.
    Raises RuntimeError on failure.
    """
    cached = get_cached_response(prompt, temperature, max_tokens)
    if cached:
        logger.info("Cached LLM response retrieved successfully.")
        return cached

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json",
    }

    models_to_try = [GROQ_MODEL, "llama-3.1-8b-instant"]

    for model in models_to_try:
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": temperature,
            "max_tokens": max_tokens,
        }

        max_retries = 3
        backoff = 1.0
        for attempt in range(max_retries):
            try:
                response = requests.post(GROQ_URL, headers=headers, json=payload, timeout=20)
                if response.status_code == 429:
                    retry_after = response.headers.get("retry-after")
                    if retry_after:
                        try:
                            sleep_time = float(retry_after)
                        except ValueError:
                            sleep_time = backoff
                    else:
                        sleep_time = backoff
                    
                    if sleep_time > 45.0:
                        logger.warning(
                            f"Model {model} hit 429 rate limit with long cooldown ({sleep_time:.2f}s). "
                            "Switching to fallback model."
                        )
                        break
                    
                    logger.warning(
                        f"Model {model} hit 429 rate limit. Retrying in {sleep_time:.2f} seconds... "
                        f"(Attempt {attempt + 1}/{max_retries})"
                    )
                    time.sleep(sleep_time)
                    backoff *= 2.0
                    continue

                response.raise_for_status()
                res_text = response.json()["choices"][0]["message"]["content"].strip()
                save_to_cache(prompt, temperature, max_tokens, res_text)
                return res_text
            except requests.RequestException as e:
                logger.warning(f"Connection error or HTTP issue for {model}: {e}. Retrying...")
                if attempt == max_retries - 1:
                    break
                time.sleep(backoff)
                backoff *= 2.0

    raise RuntimeError("LLM unavailable: all models failed or were rate limited.")


def call_llm_json(prompt: str) -> dict:
    """
    Call LLM and parse JSON from the response.
    Strips markdown fences if present.
    """
    raw = call_llm(prompt, temperature=0.0)
    # Strip ```json ... ``` if model adds it despite instructions
    clean = re.sub(r"```(?:json)?\s*", "", raw).replace("```", "").strip()
    # If the model returned extra text around the JSON, try to extract the JSON object
    if not clean.startswith("{"):
        # find the first { and the last } and attempt to parse that substring
        start = clean.find("{")
        end = clean.rfind("}")
        if start != -1 and end != -1 and end > start:
            candidate = clean[start : end + 1]
        else:
            candidate = clean
    else:
        candidate = clean

    try:
        return json.loads(candidate)
    except json.JSONDecodeError as e:
        logger.error("JSON parse failed. Raw response:\n%s\nCandidate JSON:\n%s\nError: %s", raw, candidate, e)
        raise ValueError(f"LLM returned invalid JSON: {e}\nRaw: {raw}")
