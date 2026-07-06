# app.py
import streamlit as st
import requests

# Define the backend URL
API_URL = "http://127.0.0.1:8000"

def fetch_data():
    response = requests.get(f"{API_URL}/healthcheck")
    if response.status_code == 200:
        return response.json()
    return None

# Streamlit UI
st.title("Streamlit + FastAPI Demo")
if st.button("Get Data"):
    data = fetch_data()
    if data:
        st.write(data)
    else:
        st.error("Failed to connect to API")   