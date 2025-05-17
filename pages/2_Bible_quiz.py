import streamlit as st
import json
import random

# Load the trivia data
def load_trivia_data():
    with open("bible_trivia.json", "r", encoding="utf-8") as f:
        return json.load(f)

data = load_trivia_data()

# Streamlit UI
st.title("📖 Bible Trivia Quiz")

# Difficulty selection
difficulty = st.selectbox("Choose difficulty level:", ["easy", "medium", "difficult", "kids"])

# Get questions for the selected difficulty
questions_dict = data[difficulty]
questions = list(questions_dict.items())

# Select a random question
if "current_question" not in st.session_state or st.button("🎲 New Question"):
    st.session_state.current_question = random.choice(questions)

question, answer = st.session_state.current_question

# Display question
st.markdown(f"### ❓ {question}")

# Show answer on button click
if st.button("💡 Show Answer"):
    st.success(f"✅ {answer}")



st.markdown("---")
st.caption("Developed with ❤️ by Abatan Ayodeji (Agroall) • Built using Streamlit")