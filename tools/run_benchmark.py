import json
import os
import dotenv
from main import evaluate_benchmark

# Force load latest environment variables
dotenv.load_dotenv(override=True)

print("Starting the 50-question benchmark run...")
print("This will execute queries sequentially with a 1-second pacing delay to respect Groq rate limits.")
print("Resilient exponential backoff retries are active in the LLM client.")

report = evaluate_benchmark()

# Save results
report_path = "evaluation_report.json"
with open(report_path, "w") as f:
    json.dump(report, f, indent=2)

print("\n==================================================")
print("              Evaluation Completed!               ")
print("==================================================")
print(f"Total Questions: {report['total_questions']}")
print(f"Success Count:   {report['success_count']}")
print(f"Correct Count:   {report['correct_count']}")
print(f"Failed Count:    {report['failed_count']}")
print(f"Retry Count:     {report['retry_count']}")
print(f"Execution Success Rate: {report['execution_success_rate']}")
print(f"Execution Accuracy:     {report['execution_accuracy']}")
print(f"Retry Rate:             {report['retry_rate']}")
print(f"Report successfully saved to '{report_path}'.")
print("==================================================")
