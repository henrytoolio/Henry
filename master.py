import streamlit as st
import pandas as pd
import duckdb
from pandasai import SmartDataframe
from pandasai.llm.openai import OpenAI

# --- Streamlit Setup ---
st.set_page_config(page_title="MFP DuckDB LLM App", layout="wide")
st.title("🧠 MFP Budget DuckDB + LLM Assistant")

st.markdown("""
This app lets you:
- Upload your own CSV file
- Run **SQL-style filtering** on DuckDB in-memory data
- Ask **natural language questions** using PandasAI + OpenAI
""")

# --- File Upload ---
uploaded_file = st.file_uploader("Upload your MFP budget CSV", type="csv")

if uploaded_file:
    data = pd.read_csv(uploaded_file)
    st.success("✅ File loaded successfully!")

    # --- SQL via DuckDB ---
    query = """
    SELECT *
    FROM data
    WHERE receipts_cost > 48000
    """
    result_df = duckdb.query(query).to_df()

    st.subheader("📊 Filtered Table via DuckDB")
    st.dataframe(result_df)

    # --- Natural Language Assistant ---
    st.subheader("💬 Ask the Assistant")
    user_question = st.text_input("Ask a question about the uploaded data:", "What is the average receipts cost?")

    if user_question:
        llm = OpenAI(api_token="your-openai-api-key")  # Replace with st.secrets in production
        sdf = SmartDataframe(data, config={"llm": llm})
        response = sdf.chat(user_question)
        st.markdown("**Response:**")
        st.write(response)
else:
    st.info("📂 Please upload a CSV file to begin.")
