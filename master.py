import streamlit as st
import pandas as pd
import duckdb

st.set_page_config(page_title="DuckDB Example App", layout="wide")
st.title("🦆 DuckDB + Streamlit Example")

# --- Load or create data ---
st.markdown("Running a SQL query using DuckDB on a mock DataFrame.")

data = pd.DataFrame({
    "week": [10, 11, 12, 13],
    "receipts_cost": [47609.60, 50000.12, 48200.75, 49800.40]
})

# --- Run SQL with DuckDB ---
query = """
SELECT *
FROM data
WHERE receipts_cost > 48000
"""

result = duckdb.query(query).to_df()

# --- Show Output ---
st.dataframe(result)
