import os
import streamlit as st
import pandas as pd
import duckdb

from pandasai import PandasAI
from pandasai.llm.openai import OpenAI

# --- Streamlit App Setup ---
st.set_page_config(page_title="CSV Query with PandasAI & DuckDB", layout="wide")
st.title("🗃️ CSV Query with DuckDB + 🧠 PandasAI")

# Sidebar: OpenAI API Key input
st.sidebar.header("🔑 OpenAI API Key")
api_key = st.sidebar.text_input(
    "Enter your OpenAI API Key:",
    type="password",
    help="Get your key from https://platform.openai.com/account/api-keys"
)
if not api_key:
    st.sidebar.warning("🔒 Please enter your OpenAI API Key to enable natural language querying.")
    st.stop()
os.environ["OPENAI_API_KEY"] = api_key

# File uploader
st.sidebar.header("📂 Upload CSV File")
csv_file = st.sidebar.file_uploader(
    label="Choose a CSV file",
    type=["csv"]
)

if csv_file:
    # 1. Load CSV into pandas DataFrame
    df = pd.read_csv(csv_file)
    st.success(f"Loaded {len(df)} rows and {len(df.columns)} columns.")
    st.dataframe(df.head(), use_container_width=True)

    # 2. Connect to DuckDB and register DataFrame
    con = duckdb.connect(database=":memory:")
    con.register("df", df)
    st.info("🔌 Connected to DuckDB (in-memory) and registered table 'df'.")

    # 3. Natural language query input
    st.markdown("---")
    st.header("💬 Ask your data a question")
    user_prompt = st.text_input(
        "Enter your question in plain English:",
        placeholder="e.g., 'What are the top 5 locations by sales_units?'"
    )

    if st.button("🤖 Run Query"):
        if user_prompt.strip() == "":
            st.error("Please enter a valid question.")
        else:
            with st.spinner("Processing your request with PandasAI..."):
                # Initialize LLM and agent
                llm = OpenAI()  # uses OPENAI_API_KEY from env
                pandas_ai = PandasAI(llm)
                try:
                    # Run the LLM against the DataFrame
                    result = pandas_ai.run(df, prompt=user_prompt)
                    # Display result
                    if isinstance(result, pd.DataFrame):
                        st.subheader("📊 Query Result")
                        st.dataframe(result, use_container_width=True)
                    else:
                        st.subheader("💡 Answer")
                        st.write(result)
                except Exception as e:
                    st.error(f"Error during query: {e}")

else:
    st.info("▶️ Please upload a CSV file to get started.")
