# Text-to-SQL Agentic System
**Fuse AI Fellowship 2026 — GenAI Week 3**

This repository contains a Text-to-SQL benchmark, prompt-chaining pipeline, and agentic SQL API backed by PostgreSQL.

---

## What’s in this repo

- `task1/` — Task 1 deliverables: ground truth SQL, evaluation framework, Task 1 summary, and benchmark results
- `task2/` — Task 2 deliverables: manual query decompositions for all 50 benchmark questions
- `submission/` — submission artifacts and progress tracking
- `Dockerfile` & `docker-compose.yml` — local development environment with PostgreSQL, FastAPI backend, and Streamlit UI support
- `database.py`, `sql_generator.py`, `validator.py`, `executor.py`, `main.py`, `streamlit_app.py` — core Text-to-SQL system files
- `prompts/templates.py` — prompt templates for SQL decomposition, generation, and fixes
- `seed.sql` — database seed file for the classicmodels schema
- `sql_questions_only.csv` — benchmark questions
- `evaluation_report.json` — benchmark evaluation output

---

## Setup

### Prerequisites
- Python 3.11+
- PostgreSQL (or Docker)
- `pip` installed
- `.env` file with database and API credentials

### Install dependencies

```bash
cd "c:/Users/Aaradhya/Downloads/_Organized/Fuse AI Fellowship/FUSE AIF 2026/WK3/fuseAiF_wk3_text2sql"
pip install -r requirements.txt
```

### Configure environment

Create a `.env` file with the required values.
Use `.env.example` as a template if available.

Required environment variables:
- `DB_HOST`
- `DB_PORT`
- `DB_NAME`
- `DB_USER`
- `DB_PASSWORD`
- `OPENAI_API_KEY` (or provider-specific API key if configured)

### Database seed

Load the PostgreSQL database with `seed.sql`.
If using Docker, `docker-compose.yml` should mount and initialize the database automatically.

---

## Run locally

### Option 1: Python

```bash
python main.py
```

or

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Option 2: Streamlit UI

Start the backend first with one of the Python commands above, then run Streamlit in a second terminal:

```bash
python -m streamlit run streamlit_app.py
```

Open `http://localhost:8501` in your browser. The Streamlit UI sends requests to `http://localhost:8000/agent/sql` by default.

### Option 3: Docker

```bash
docker compose up --build
```

The API app should be available at `http://localhost:8000` and the Streamlit UI at `http://localhost:8501`.

---

## API Endpoints

### Health check

```
GET /health
```

### SQL pipeline endpoint

```
POST /pipeline/sql
Content-Type: application/json

{ "question": "Count customers per country" }
```

### Agent endpoint

```
POST /agent/sql
Content-Type: application/json

{ "question": "How many shipped orders are from USA customers?" }
```

### Benchmark evaluation

```
GET /evaluate
```

This endpoint runs the benchmark questions and returns aggregated performance metrics.
The latest benchmark run is saved in `evaluation_report.json` and contains the full 50-question agent report.

Current report summary:

- total_questions: 50
- execution_success_rate: 16.0%
- execution_accuracy: 6.0%
- retry_rate: 0.0%
- success_count: 8
- correct_count: 3
- failed_count: 42

The JSON file includes per-question generated SQL, execution outcome, correctness, retry status, and summary text.

---

## Project structure

```
.
├── Dockerfile
├── docker-compose.yml
├── README.md
├── database.py
├── docker-compose.yml
├── evaluation_report.json
├── executor.py
├── llm_client.py
├── main.py
├── prompts/
│   └── templates.py
├── requirements.txt
├── seed.sql
├── sql_generator.py
├── sql_questions_only.csv
├── task1/
│   ├── Task1_Completion_Summary.md
│   ├── Task1_Part1_Ground_Truth.md
│   ├── Task1_Part2_Evaluation_Framework.md
│   ├── Task1_Part2_Evaluation_Strategy.md
│   ├── generate_task1_part1.py
│   └── task1_ground_truth_results.json
├── task2/
│   └── Task2_Query_Decompositions.md
├── submission/
│   ├── Week3_GenAI_Submission.md
│   ├── Week3_Task_Plan.md
│   └── task_progress.md
└── test_agent.py
```

---

## Key notes

- The system is designed for **SELECT-only** SQL generation.
- All database column names in classicmodels use camelCase and should be double-quoted in SQL, e.g. `"customerNumber"`.
- Task 1 provides the benchmark ground truth and evaluation framework.
- Task 2 contains manual decompositions for all 50 benchmark questions.

---

## Useful files

- `task1/Task1_Part1_Ground_Truth.md` — ground truth SQL and query results
- `task1/Task1_Part2_Evaluation_Framework.md` — evaluation methodology and metrics
- `task2/Task2_Query_Decompositions.md` — intent/tables/columns/filters/joins/aggregation for each benchmark question
- `task_progress.md` — current progress and status

---

## Docker notes

The included `docker-compose.yml` starts a PostgreSQL container seeded from `seed.sql` and runs the app container.

Use `docker compose up --build` to start the environment.

---

## Next steps

1. Complete Task 2: decompose all benchmark questions
2. Build Task 3: prompt-chaining Text-to-SQL pipeline
3. Build Task 4: FastAPI SQL agent with retry and summarization
4. Run benchmark evaluation and update `evaluation_report.json`


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

