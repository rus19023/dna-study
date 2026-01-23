FLASHCARDS = [
    {"question": "What is the powerhouse of the cell?", "answer": "Mitochondria"},
    {"question": "State Newton’s 2nd Law.", "answer": "F = ma"},
    {"question": "What is an eigenvalue?", "answer": "A scalar associated with a linear transformation"},
]



# import streamlit as st
# import random

# # ---- FLASHCARDS ----
# # Replace or extend this list with your course content!
# flashcards = [
#     {"question": "What is the powerhouse of the cell?", "answer": "Mitochondria"},
#     {"question": "Define Newton's 2nd Law.", 
#      "answer": "Force equals mass times acceleration (F = ma)"},
#     {"question": "What is the capital of France?", "answer": "Paris"},
#     {"question": "What is the integral of 1/x dx?", "answer": "ln|x| + C"},
# ]

# # ---- SESSION STATE SETUP ----
# if "card_index" not in st.session_state:
#     st.session_state.card_index = 0

# if "show_answer" not in st.session_state:
#     st.session_state.show_answer = False

# # ---- FUNCTIONS ----
# def next_card():
#     st.session_state.card_index = (st.session_state.card_index + 1) % len(flashcards)
#     st.session_state.show_answer = False

# def flip_card():
#     st.session_state.show_answer = not st.session_state.show_answer

# # ---- UI ----
# st.title("📘 College Flashcards Study Tool")

# # Current flashcard
# card = flashcards[st.session_state.card_index]

# st.write(
#     "<div style='font-size:24px; font-weight:bold; padding:10px; border:1px solid lightgray;'>"
#     + (card["answer"] if st.session_state.show_answer else card["question"])
#     + "</div>",
#     unsafe_allow_html=True,
# )

# # Buttons
# col1, col2 = st.columns(2)
# with col1:
#     st.button("🔄 Flip Card", on_click=flip_card)
# with col2:
#     st.button("➡️ Next Card", on_click=next_card)

# # Progress
# st.write(f"*Card {st.session_state.card_index + 1} of {len(flashcards)}*")
