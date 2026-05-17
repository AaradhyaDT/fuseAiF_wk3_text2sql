import json
import os

import requests
import streamlit as st

API_URL = os.getenv("API_URL", "http://localhost:8000")
AGENT_ENDPOINT = f"{API_URL.rstrip('/')}/agent/sql"

st.set_page_config(
    page_title="Text-to-SQL Agent",
    page_icon="🧠",
    layout="wide",
)

st.title("Text-to-SQL Agent")
st.markdown(
    "A simple Streamlit UI for the Fuse AI Fellowship Week 3 SQL agent. "
    "Enter a natural language question and run the agent via the `/agent/sql` endpoint."
)

question = st.text_area(
    "Natural language question",
    value="How many shipped orders are from USA customers?",
    height=120,
)

col1, col2 = st.columns([3, 1])
with col1:
    if st.button("Run agent"):
        if not question.strip():
            st.error("Please enter a question before running the agent.")
        else:
            payload = {"question": question}
            try:
                response = requests.post(AGENT_ENDPOINT, json=payload, timeout=60)
                response.raise_for_status()
                data = response.json()
            except requests.RequestException as exc:
                st.error(f"Agent request failed: {exc}")
                st.markdown(f"**Target endpoint:** `{AGENT_ENDPOINT}`")
                st.stop()

            st.success("Agent call completed")
            st.subheader("Generated SQL")
            st.code(data.get("sql", ""), language="sql")

            st.subheader("Agent summary")
            st.write(data.get("summary", "No summary returned."))

            st.subheader("Execution metadata")
            st.write(
                {
                    "status": data.get("status"),
                    "attempts": data.get("attempts"),
                    "retried": data.get("retried"),
                    "execution_time_ms": data.get("execution_time_ms"),
                }
            )

            st.subheader("Result rows")
            result = data.get("result", {})
            rows = result.get("rows", [])
            if rows:
                st.table(rows)
            else:
                st.write(result)

            with st.expander("Raw JSON response"):
                st.json(data)

with col2:
    st.markdown("### Configuration")
    st.write(f"**API URL:** `{AGENT_ENDPOINT}`")
    st.info(
        "Run the FastAPI app first, then use this UI to send questions to `/agent/sql`."
    )
    st.markdown(
        "If you are running with Docker Compose, the Streamlit UI is available on port 8501."
    )
    st.markdown(
        "If the FastAPI app is local, set `API_URL=http://localhost:8000` before launching Streamlit."
    )
