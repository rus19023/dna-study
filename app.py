# app.py - TEMPORARY DEBUG VERSION
import streamlit as st

st.set_page_config(
    page_title="Flashcard Study",
    page_icon="🧬",
)

st.title("Debug Test")
st.write("Step 1: Basic streamlit works")

try:
    from data.db import users
    st.success("Step 2: MongoDB connection works")
    count = users.count_documents({})
    st.write(f"Found {count} users")
except Exception as e:
    st.error(f"MongoDB error: {e}")

try:
    from ui.auth import handle_authentication
    st.success("Step 3: Auth import works")
except Exception as e:
    st.error(f"Auth import error: {e}")

try:
    from ui.study_tab import render_study_tab
    st.success("Step 4: Study tab import works")
except Exception as e:
    st.error(f"Study tab import error: {e}")

st.write("If you see this, check which steps failed above!")