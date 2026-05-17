import json
import os
from prompts.templates import DECOMPOSITION_PROMPT, SQL_GENERATION_PROMPT, SCHEMA_CONTEXT

queries_file = "logs/queries.jsonl"
cache_file = "logs/llm_cache.json"

if not os.path.exists(queries_file):
    print("No queries.jsonl found. Skipping prepopulation.")
    exit(0)

# Load current cache if exists
cache = {}
if os.path.exists(cache_file):
    try:
        with open(cache_file, "r", encoding="utf-8") as f:
            cache = json.load(f)
    except Exception:
        pass

print(f"Reading from {queries_file}...")
count = 0
with open(queries_file, "r", encoding="utf-8") as f:
    for line in f:
        if not line.strip():
            continue
        try:
            data = json.loads(line)
            question = data.get("question")
            decomposition = data.get("decomposition")
            sql = data.get("sql")
            status = data.get("status")

            # Only cache successful queries
            if not question or not decomposition or not sql or status != "success":
                continue

            # 1. Cache Decomposition
            decomp_prompt = DECOMPOSITION_PROMPT.format(schema=SCHEMA_CONTEXT, question=question)
            decomp_key = f"{decomp_prompt}_0.0_1024"
            if decomp_key not in cache:
                cache[decomp_key] = json.dumps(decomposition)
                count += 1

            # 2. Cache SQL Generation
            sql_prompt = SQL_GENERATION_PROMPT.format(
                schema=SCHEMA_CONTEXT,
                decomposition=json.dumps(decomposition, indent=2)
            )
            sql_key = f"{sql_prompt}_0.0_1024"
            if sql_key not in cache:
                cache[sql_key] = sql
                count += 1

        except Exception as e:
            print(f"Error parsing line: {e}")

# Save back to cache
os.makedirs(os.path.dirname(cache_file), exist_ok=True)
with open(cache_file, "w", encoding="utf-8") as f:
    json.dump(cache, f, indent=2)

print(f"Cache pre-population complete! Added {count} entries.")
