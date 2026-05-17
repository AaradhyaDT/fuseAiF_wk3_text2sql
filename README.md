# Text-to-SQL Agentic System
**Fuse AI Fellowship 2026 — GenAI Week 3**

A production-style Text-to-SQL pipeline and agentic API built on FastAPI + PostgreSQL,
using Groq (free LLM API) for natural language understanding and SQL generation.

---

## Architecture

```
Natural Language Question
        │
        ▼
┌───────────────────┐
│  Decomposition    │  llama-3.3-70b via Groq
│  (sql_generator)  │  → intent, tables, columns, filters, joins
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│  SQL Generation   │  LLM prompt → raw SQL string
│  (sql_generator)  │
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│  Validation       │  Blocks INSERT/UPDATE/DELETE/DROP etc.
│  (validator)      │
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│  Execution        │  psycopg2 → PostgreSQL
│  (executor)       │  Statement timeout: 10s
└────────┬──────────┘
         │ Error?
         ▼
┌───────────────────┐
│  LLM Fix + Retry  │  Up to 3 retries (agent) / 1 retry (pipeline)
│  (executor)       │
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│  Summary          │  LLM → human-readable answer sentence
│  (main.py)        │
└───────────────────┘
```

---

## Setup

### 1. Prerequisites
- Python 3.11+
- PostgreSQL with classicmodels database loaded (`seed.sql`)
- Free Groq API key: https://console.groq.com

### 2. Install dependencies
```bash
cd text2sql
pip install -r requirements.txt
```

### 3. Configure
Edit `database.py` only if you want to override defaults. It now reads credentials from environment variables:
- `DB_HOST`
- `DB_PORT`
- `DB_NAME`
- `DB_USER`
- `DB_PASSWORD`
- `GROQ_API_KEY`

Create a `.env` file from the example:
```powershell
copy .env.example .env
```

Then fill in your values in `.env`.

Set your Groq API key by editing `.env` or exporting it in your shell:
```powershell
$env:GROQ_API_KEY = "gsk_your_key_here"
```

Avoid hardcoding credentials directly in `llm_client.py`.

### 4. Copy benchmark CSV
```bash
cp /path/to/sql_questions_only.csv ./
```

### 5. Run the server
```bash
python main.py
# or
uvicorn main:app --reload --port 8000
```

---

## API Endpoints

### Health Check
```
GET /health
```
```json
{"status": "ok", "db_connected": true}
```

---

### Task 3 — Pipeline (1 retry)
```
POST /pipeline/sql
Content-Type: application/json

{"question": "Count customers per country"}
```

**Response:**
```json
{
  "question": "Count customers per country",
  "decomposition": {
    "intent": "Count customers grouped by country",
    "tables": ["customers"],
    "columns": ["country", "COUNT(customerNumber)"],
    "filters": [],
    "joins": [],
    "aggregation": "COUNT",
    "group_by": ["country"]
  },
  "sql": "SELECT \"country\", COUNT(\"customerNumber\") AS customerCount FROM customers GROUP BY \"country\" ORDER BY customerCount DESC;",
  "result": {
    "columns": ["country", "customerCount"],
    "rows": [{"country": "USA", "customerCount": 36}, ...],
    "row_count": 27,
    "execution_time_ms": 8.4,
    "error": null
  },
  "status": "success",
  "attempts": 1,
  "retried": false,
  "execution_time_ms": 1240.5
}
```

---

### Task 4 — Agent (3 retries + summary)
```
POST /agent/sql
Content-Type: application/json

{"question": "How many shipped orders are from USA customers?"}
```

**Response:**
```json
{
  "question": "How many shipped orders are from USA customers?",
  "decomposition": {...},
  "sql": "SELECT COUNT(*) FROM orders o JOIN customers c ON o.\"customerNumber\" = c.\"customerNumber\" WHERE c.\"country\" = 'USA' AND o.\"status\" = 'Shipped';",
  "result": {"rows": [{"count": 46}], "row_count": 1, "error": null, ...},
  "summary": "There are 46 shipped orders from customers in the USA.",
  "status": "success",
  "attempts": 1,
  "retried": false,
  "execution_time_ms": 1874.3
}
```

---

### Benchmark Evaluation
```
GET /evaluate
```
Runs all 50 benchmark questions through the agent and returns:
```json
{
  "total_questions": 50,
  "success_count": 46,
  "failed_count": 4,
  "retry_count": 3,
  "execution_success_rate": "92.0%",
  "retry_rate": "6.0%",
  "results": [...]
}
```

---

## Project Structure

```
text2sql/
├── main.py                         # FastAPI app (Task 3 + Task 4 endpoints)
├── database.py                     # PostgreSQL connection + query execution
├── validator.py                    # SQL safety validation
├── sql_generator.py                # LLM decompose + generate SQL
├── executor.py                     # Execute with retry logic
├── llm_client.py                   # Groq API wrapper
├── requirements.txt
├── sql_questions_only.csv          # Benchmark dataset (copy here)
├── prompts/
│   └── templates.py                # All LLM prompt templates
├── logs/
│   ├── app.log                     # Application logs
│   └── queries.jsonl               # Per-query structured log
├── Task1_Part2_Evaluation_Strategy.md
└── Task2_Query_Decompositions.md
```

---

## Safety Design

- `validator.py` blocks any non-SELECT SQL before it reaches PostgreSQL
- Statement timeout (10s) prevents runaway queries
- Multiple statement injection blocked (`;` stacking)
- All executions logged to `logs/queries.jsonl`
- LLM fix prompts are sandboxed — they cannot execute arbitrary code

---

## LLM Free Alternatives

The system uses **Groq** by default (free, fast llama-3.3-70b).
Other free alternatives:
- **Google AI Studio** (Gemini): https://aistudio.google.com
- **OpenRouter** (free tier): https://openrouter.ai
- **Ollama** (local, no API key): https://ollama.com

To switch, modify `llm_client.py` to point to the provider's API endpoint.

---

## Docker (optional)

Quick Docker setup to run the API and a local PostgreSQL DB using `docker-compose`.

1. Build and run (from project root):

```bash
docker compose up --build
```

2. The API will be available at http://localhost:8000.

3. By default `docker-compose.yml` seeds the database using `seed.sql`. Adjust credentials by editing `.env` or the `docker-compose.yml` environment section.

4. Useful commands:

```bash
# Build only
docker compose build

# Start in background
docker compose up -d

# Stop and remove containers
docker compose down -v

# View logs
docker compose logs -f
```

Notes:
- The `Dockerfile` uses Python 3.11-slim. The app reads DB config from environment variables, so Docker Compose wires the `db` service hostname for you.
- If you already have a local Postgres instance on 5432, stop it or change port mapping in `docker-compose.yml`.

