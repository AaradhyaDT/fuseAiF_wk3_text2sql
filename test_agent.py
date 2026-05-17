import json
import traceback
from main import agent_sql, QuestionRequest

try:
    resp = agent_sql(QuestionRequest(question="List all products"))
    print(json.dumps(resp, default=str, indent=2))
except Exception as e:
    traceback.print_exc()
    print('EXCEPTION:', e)
