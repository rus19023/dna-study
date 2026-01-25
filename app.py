# app.py

import streamlit as st

from core.state import init_state
from core.scoring import calculate_points
from ui.layout import render_header
from ui.components import flashcard_box, controls, answer_buttons, user_stats, leaderboard

PAGE_TITLE = "Flashcard Study App"

st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon="🧬",  # You can use an emoji or path to an image file
    layout="wide"  # Optional: makes the app use full width
)

from data.deck_store import get_deck_names, get_deck, add_card
from data.user_store import (
    get_all_usernames, 
    create_user, 
    get_user, 
    update_user_score,
    get_leaderboard
)


# ----------------------------
# Sidebar: User Login/Registration
# ----------------------------
st.sidebar.title("🧬 Flashcard Study")

if "logged_in_user" not in st.session_state:
    st.session_state.logged_in_user = None

# Show login/register only if NOT logged in
if not st.session_state.logged_in_user:
    # Login/Register toggle
    auth_mode = st.sidebar.radio("", ["Login", "Register"])

    if auth_mode == "Login":
        username = st.sidebar.text_input("Username", key="login_username")
        password = st.sidebar.text_input("Password", type="password", key="login_password")
        
        if st.sidebar.button("Login"):
            if username.strip() and password.strip():
                user = get_user(username.strip())
                if user and user.get("password") == password:
                    st.session_state.logged_in_user = username.strip()
                    st.rerun()
                else:
                    st.sidebar.error("Invalid username or password")
            else:
                st.sidebar.error("Please enter username and password")

    else:  # Register
        new_username = st.sidebar.text_input("Choose Username", key="reg_username")
        new_password = st.sidebar.text_input("Choose Password", type="password", key="reg_password")
        confirm_password = st.sidebar.text_input("Confirm Password", type="password", key="reg_confirm")
        
        if st.sidebar.button("Register"):
            if new_username.strip() and new_password.strip():
                if new_password != confirm_password:
                    st.sidebar.error("Passwords don't match")
                elif get_user(new_username.strip()):
                    st.sidebar.error("Username already exists")
                else:
                    create_user(new_username.strip(), new_password)
                    st.sidebar.success(f"User '{new_username}' created! Please login.")
            else:
                st.sidebar.error("Please fill all fields")

    # Stop if not logged in
    st.title("🧬 Flashcard Study App")
    st.info("Please login or register in the sidebar to continue.")
    st.stop()

# Show logout and deck selection only if logged in
else:
    st.sidebar.write(f"👤 Logged in as: **{st.session_state.logged_in_user}**")
    
    if st.sidebar.button("Logout"):
        st.session_state.logged_in_user = None
        st.rerun()

    st.sidebar.divider()

    # ----------------------------
    # Sidebar: Deck Selection
    # ----------------------------
    deck_names = get_deck_names()

    if not deck_names:
        st.error("No decks found in database.")
        st.stop()

    deck_name = st.sidebar.selectbox(
        "Choose a deck",
        options=deck_names
    )

    st.sidebar.divider()

st.sidebar.divider()
# ----------------------------
# Main Page
# ----------------------------
st.title("🧬 Flashcard Study App")

# Load user data
current_user = get_user(st.session_state.logged_in_user)
if not current_user:
    st.error("User not found")
    st.stop()

st.divider()

# Track deck changes
if "current_deck" not in st.session_state or st.session_state.current_deck != deck_name:
    st.session_state.current_deck = deck_name
    if "cards" in st.session_state:
        del st.session_state.cards

# Load cards for selected deck
cards = get_deck(deck_name)

# ----------------------------
# Tabs
# ----------------------------
tab1, tab2, tab3, tab4 = st.tabs(["📚 Study", "📊 Stats", "🏆 Leaderboard", "➕ Add Card"])

# ----------------------------
# Tab 1: Flashcard Study
# ----------------------------
with tab1:
    if not cards:
        st.warning(f"The deck '{deck_name}' is empty. Add some cards in the 'Add Card' tab!")
    else:
        init_state(cards)
        
        # Initialize session streak if not exists
        if "session_streak" not in st.session_state:
            st.session_state.session_streak = 0

        card = st.session_state.cards[st.session_state.index]
        text = card["answer"] if st.session_state.show_answer else card["question"]

        flashcard_box(text)
        
        # Show different controls based on whether answer is shown
        if not st.session_state.show_answer:
            controls()
        else:
            # Answer feedback buttons
            def handle_correct():
                points = calculate_points(True)
                update_user_score(st.session_state.logged_in_user, points, correct=True)
                st.session_state.session_streak += 1
                # Move to next card
                st.session_state.index = (st.session_state.index + 1) % len(st.session_state.cards)
                st.session_state.show_answer = False
                
            def handle_incorrect():
                points = calculate_points(False)
                update_user_score(st.session_state.logged_in_user, points, correct=False)
                st.session_state.session_streak = 0
                # Move to next card
                st.session_state.index = (st.session_state.index + 1) % len(st.session_state.cards)
                st.session_state.show_answer = False
            
            answer_buttons(on_correct=handle_correct, on_incorrect=handle_incorrect)

        st.write(
            f"Card {st.session_state.index + 1} of {len(st.session_state.cards)}"
        )
        
        st.write(f"Session Streak: {st.session_state.session_streak} 🔥")

# ----------------------------
# Tab 2: Stats
# ----------------------------
with tab2:
    st.subheader("Your Statistics")
    user_stats(current_user)
    
    # Could add more detailed stats here
    st.divider()
    st.write("### Additional Stats")
    
    total = current_user["cards_studied"]
    if total > 0:
        st.write(f"**Best Streak:** {current_user.get('best_streak', 0)} 🔥")
        st.write(f"**Total Cards Studied:** {total}")
        st.write(f"**Correct Answers:** {current_user['correct_answers']}")
        st.write(f"**Incorrect Answers:** {current_user['incorrect_answers']}")
    else:
        st.info("Start studying to see your stats!")

# ----------------------------
# Tab 3: Leaderboard
# ----------------------------
with tab3:
    top_users = get_leaderboard(limit=10)
    leaderboard(top_users)

# ----------------------------
# Tab 4: Add New Card
# ----------------------------
with tab4:
    st.subheader("Add a New Flashcard")
    
    # Option to select existing deck or create new one
    deck_option = st.radio(
        "Choose deck:",
        options=["Add to existing deck", "Create new deck"]
    )
    
    if deck_option == "Add to existing deck":
        existing_decks = get_deck_names()
        if existing_decks:
            add_to_deck = st.selectbox(
                "Select deck:",
                options=existing_decks,
                key="add_card_deck"
            )
        else:
            st.warning("No decks exist yet. Please create a new deck below.")
            deck_option = "Create new deck"
    
    if deck_option == "Create new deck":
        add_to_deck = st.text_input("New deck name:", key="new_deck_name")
    
    with st.form("add_card_form"):
        new_question = st.text_area("Question", height=100)
        new_answer = st.text_area("Answer", height=100)

        submitted = st.form_submit_button("Add card")

        if submitted:
            if deck_option == "Create new deck" and not add_to_deck.strip():
                st.error("Please enter a deck name.")
            elif not new_question.strip() or not new_answer.strip():
                st.error("Both question and answer are required.")
            else:
                add_card(
                    add_to_deck.strip(),
                    new_question.strip(),
                    new_answer.strip()
                )

                st.success(f"Flashcard added to '{add_to_deck.strip()}'!")
                
                # Clear session state and reload
                logged_in = st.session_state.logged_in_user
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.session_state.logged_in_user = logged_in
                st.rerun()