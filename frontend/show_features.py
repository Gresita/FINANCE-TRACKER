import streamlit as st
import requests

st.set_page_config(page_title="Python Advanced Features", layout="centered")
st.title("🐍 Python Advanced")

features = [
    "Variables",
    "Loops",
    "Conditional Statements",
    "Functions",
    "Data Structure",
    "Object-Oriented Programming (OOP)",
    "Error Handling",
    "Data Manipulation & Visualization",
    "API Development",
    "Web Scraping",
    "Database Management",
    "Authentication & Authorization",
    "Project Structure",
    "Originality",
    "Functionality"
]

st.markdown("### Features List:")
for feature in features:
    st.markdown(f"- {feature}")

st.sidebar.image("https://www.python.org/static/community_logos/python-logo.png", width=150)

st.markdown("---")

# Trego mesazhin nga backend
try:
    response = requests.get("http://127.0.0.1:8000/")
    if response.status_code == 200:
        data = response.json()
        st.success("Backend status: " + str(data))
    else:
        st.warning("Backend returned status code: " + str(response.status_code))
except Exception as e:
    st.error(f"Could not connect to backend: {e}")