# Task Progress

## Current status

- Task 1 is complete: ground truth SQL and evaluation framework have been generated.
- Generated `Task1_Part1_Ground_Truth.md`, `Task1_Part2_Evaluation_Framework.md`, and `Task1_Completion_Summary.md`.
- Verified database connectivity and executed all 50 benchmark queries successfully.
- Dockerized the project: `Dockerfile`, `docker-compose.yml`, and `.dockerignore` created.
- Updated `README.md` with Docker setup and run instructions.
- Verified the service is reachable at `http://localhost:8000/health` inside Docker.
- Added `evaluation_report.json` for benchmark output.
- Appended an automated evaluation summary to `Week3_GenAI_Submission.md`.

## Completed tasks

- [x] Add Dockerfile for app
- [x] Add docker-compose with Postgres service and seed
- [x] Add .dockerignore
- [x] Update README with Docker instructions
- [x] Build and test Docker containers locally
- [x] Run benchmark and collect evaluation report
- [x] Complete Task 1: ground truth SQL queries and evaluation framework

## Remaining tasks

- [ ] Add the full benchmark report details to the submission package
- [ ] Prepare final submission artifacts (screenshots, final README review)
- [ ] Start Task 2: manual query decomposition for all 50 questions
- [ ] Start Task 3: build Text-to-SQL pipeline and evaluation harness
- [ ] Start Task 4: build FastAPI SQL agent and benchmark via endpoint

## Notes

- Task 1 now has 0 execution failures and full ground truth documentation.
- Task 2 is the next priority: decompose all 50 benchmark questions into intent, tables, columns, filters, joins, and aggregation.
- Once Task 2 is complete, Task 3 can be built on top of the completed benchmark and evaluation framework.
