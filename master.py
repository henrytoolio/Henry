import streamlit as st
import pandas as pd
from pandasai import PandasAI
from pandasai.llm.openai import OpenAI
import os

# --- Streamlit Setup ---
st.set_page_config(
    page_title="Data Analysis Assistant",
    page_icon="🧠",
    layout="wide"
)

# Check for API key
if 'OPENAI_API_KEY' not in st.secrets:
    st.error("⚠️ OpenAI API key not found!")
    st.markdown("""
    To use this app, you need to set up your OpenAI API key:
    1. Go to [OpenAI Platform](https://platform.openai.com/api-keys)
    2. Create a new API key
    3. Create a `.streamlit/secrets.toml` file in your project directory
    4. Add your API key like this:
    ```toml
    OPENAI_API_KEY = "your-api-key-here"
    ```
    """)
    st.stop()

st.title("🧠 Data Analysis Assistant")

st.markdown("""
This app allows you to:
- Upload your own CSV file
- Ask questions about your data in natural language
- Get insights and visualizations automatically
""")

# --- File Upload ---
st.subheader("Step 1: Upload your CSV file")
uploaded_file = st.file_uploader("Choose a CSV file to analyze", type="csv")

if uploaded_file is None:
    st.info("📂 Please upload a CSV file to begin.")
    st.stop()

# --- Data Loading and Overview ---
try:
    data = pd.read_csv(uploaded_file)
    st.success("✅ File loaded successfully!")
    
    st.subheader("Step 2: Dataset Overview")
    col1, col2 = st.columns(2)
    with col1:
        st.write("Dataset Shape:", data.shape)
        st.write("Columns:", list(data.columns))
    with col2:
        st.write("Sample Data:")
        st.dataframe(data.head())
except Exception as e:
    st.error(f"Error loading file: {str(e)}")
    st.stop()

# --- Natural Language Query Section ---
st.subheader("Step 3: Ask Questions About Your Data")
user_question = st.text_input(
    "Ask a question about your data:",
    placeholder="Example: What is the average value of column X? or Show me a correlation between columns X and Y"
)

if user_question:
    with st.spinner("Analyzing your data..."):
        try:
            llm = OpenAI(api_token=st.secrets["OPENAI_API_KEY"])
            pandas_ai = PandasAI(llm)
            response = pandas_ai.run(data, prompt=user_question)
            st.subheader("📈 Analysis Results")
            if isinstance(response, pd.DataFrame):
                st.dataframe(response)
            else:
                st.write(response)
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            st.info("Try rephrasing your question or checking if the columns you're referring to exist in the dataset.")

else:
    st.info("📂 Please upload a CSV file to begin.")
