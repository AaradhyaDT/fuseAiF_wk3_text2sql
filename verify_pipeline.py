"""
verify_pipeline.py — End-to-End Diagnostic and Verification Script
Fuse AI Fellowship 2026 — GenAI Week 3

This script performs diagnostic checks on:
1. Environment configuration (.env parsing)
2. Groq LLM API connectivity
3. PostgreSQL connection pool and classicmodels database seeding
4. Pipeline routing (deconstruct -> generate -> safe execute)
"""

import os
import sys
import io
import json
import logging
from pathlib import Path
from dotenv import load_dotenv

# Enforce UTF-8 encoding for standard output/error to prevent UnicodeEncodeError on Windows
if sys.platform.startswith("win"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

# Set up simple console logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

def check_env():
    print("\n--- [STAGE 1] Checking Environment Variables ---")
    env_path = Path(".env")
    if not env_path.exists():
        print("❌ ERROR: .env file is missing. Please create it from .env.example.")
        return False
    
    load_dotenv(override=True)
    groq_key = os.getenv("GROQ_API_KEY")
    if not groq_key or groq_key.strip() == "":
        print("⚠️ WARNING: GROQ_API_KEY is not defined in .env. LLM calls will fail until you provide a key.")
    else:
        print(f"✓ GROQ_API_KEY is configured (starts with: {groq_key[:6]}...)")
        
    print(f"✓ DB_HOST: {os.getenv('DB_HOST', 'localhost')}")
    print(f"✓ DB_PORT: {os.getenv('DB_PORT', '5432')}")
    print(f"✓ DB_NAME: {os.getenv('DB_NAME', 'classicmodels')}")
    print(f"✓ DB_USER: {os.getenv('DB_USER', 'postgres')}")
    return True

def check_llm():
    print("\n--- [STAGE 2] Checking Groq LLM Connectivity ---")
    try:
        from llm_client import call_llm
        prompt = "Hello! Answer in exactly five words."
        print(f"Sending test prompt: '{prompt}'")
        response = call_llm(prompt)
        print(f"✓ LLM Response: '{response}'")
        return True
    except Exception as e:
        print(f"❌ ERROR: LLM call failed. Reason: {e}")
        print("👉 Tip: Double check your GROQ_API_KEY in .env and verify internet access.")
        return False

def check_db():
    print("\n--- [STAGE 3] Checking PostgreSQL Database ---")
    try:
        from database import test_connection, get_connection
        if test_connection():
            print("✓ Database connection successful!")
            # Try to query the table list to make sure classicmodels is seeded
            with get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        SELECT table_name 
                        FROM information_schema.tables 
                        WHERE table_schema = 'public';
                    """)
                    tables = [row[0] for row in cur.fetchall()]
                    print(f"✓ Public tables found: {', '.join(tables) if tables else 'None'}")
                    if "products" in tables and "customers" in tables:
                        print("✓ Database contains 'products' and 'customers' tables. Seeding verified!")
                    else:
                        print("⚠️ WARNING: The 'classicmodels' database appears to be empty. Please run 'seed.sql' to initialize the schema and data.")
            return True
        else:
            print("❌ ERROR: Database test_connection returned False.")
            print("👉 Diagnostics: Verify your local PostgreSQL server is running and DB credentials in .env are correct.")
            return False
    except Exception as e:
        print(f"❌ ERROR: Database check raised an exception: {e}")
        return False

def check_pipeline():
    print("\n--- [STAGE 4] Checking E2E Pipeline ---")
    try:
        from sql_generator import decompose_question, generate_sql
        from executor import run_with_retry
        
        question = "How many customers are from USA?"
        print(f"Test Question: '{question}'")
        
        # Decompose
        print("Running decomposition...")
        decomp = decompose_question(question)
        print(f"Decomposition:\n{json.dumps(decomp, indent=2)}")
        
        # Generate SQL
        print("Compiling SQL...")
        sql = generate_sql(decomp)
        print(f"Generated SQL: {sql}")
        
        # Execute safely
        print("Executing SQL with validation guard...")
        exec_res = run_with_retry(sql, max_retries=1)
        print(f"Execution Result:\n{json.dumps(exec_res, indent=2)}")
        
        if exec_res["status"] == "success":
            print("\n🎉 SUCCESS: The GenAI Text-to-SQL pipeline is fully working!")
        else:
            print("\n❌ PIPELINE FAILURE: SQL was generated but failed execution.")
            
    except Exception as e:
        print(f"❌ ERROR: Pipeline run crashed. Reason: {e}")

if __name__ == "__main__":
    print("==================================================")
    print("       Text-to-SQL Pipeline Diagnostics           ")
    print("==================================================")
    
    env_ok = check_env()
    llm_ok = False
    db_ok = False
    
    if env_ok:
        llm_ok = check_llm()
        db_ok = check_db()
        
    if llm_ok and db_ok:
        check_pipeline()
    else:
        print("\n🛑 Verification halted: Please resolve the LLM/DB connection errors above before running the full pipeline.")
    print("==================================================")
