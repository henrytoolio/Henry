import streamlit as st
import pandas as pd
import duckdb

# --- Streamlit Setup ---
st.set_page_config(
    page_title="DuckDB SQL Query Tool",
    page_icon="🦆",
    layout="wide"
)

st.title("🦆 DuckDB SQL Query Tool")

st.markdown("""
Upload a CSV file and run SQL queries on it using DuckDB. 
- The uploaded data will be available as a table named `data`.
- Enter your SQL query below and see the results instantly!
""")

# --- File Upload ---
st.subheader("Step 1: Upload your CSV file")
uploaded_file = st.file_uploader("Choose a CSV file to analyze", type="csv")

if uploaded_file is None:
    st.info("📂 Please upload a CSV file to begin.")
    st.stop()

# --- Data Loading ---
try:
    data = pd.read_csv(uploaded_file)
    st.success("✅ File loaded successfully!")
    st.write("Preview of uploaded data:")
    st.dataframe(data.head())
except Exception as e:
    st.error(f"Error loading file: {str(e)}")
    st.stop()

# --- SQL Query Section ---
st.subheader("Step 2: Enter your DuckDB SQL query")
def_sql = """SELECT * FROM data LIMIT 5"""
user_sql = st.text_area("SQL Query", value=def_sql, height=100)

if st.button("Run Query"):
    try:
        con = duckdb.connect()
        con.register("data", data)
        result = con.execute(user_sql).fetchdf()
        st.success("Query executed successfully!")
        st.dataframe(result)
        con.close()
    except Exception as e:
        st.error(f"Error running query: {str(e)}")


else:
    st.info("📂 Please upload a CSV file to begin.")
