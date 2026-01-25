# ui/components.py

import streamlit as st
from core.flashcard_logic import flip_card, next_card


def flashcard_box(text):
    st.markdown(
        f"""
        <div style="
            font-size:24px;
            padding:20px;
            border-radius:10px;
            border:2px solid #ddd;
            text-align:center;
            min-height:200px;
            display:flex;
            align-items:center;
            justify-content:center;">
            {text}
        </div>
        """,
        unsafe_allow_html=True
    )
    

def controls():
    col1, col2 = st.columns(2)
    with col1:
        st.button("🔄 Flip", key="flip_btn", on_click=flip_card, use_container_width=True)
    with col2:
        st.button("➡️ Next", key="next_btn", on_click=next_card, use_container_width=True)


def answer_buttons(on_correct, on_incorrect):
    """Show Got it / Need practice buttons after flipping"""
    col1, col2 = st.columns(2)
    with col1:
        st.button("✓ Got it!", key="correct_btn", on_click=on_correct, use_container_width=True, type="primary")
    with col2:
        st.button("✗ Need practice", key="incorrect_btn", on_click=on_incorrect, use_container_width=True)


def user_stats(user_data):
    """Display user statistics"""
    col1, col2, col3, col4 = st.columns(4)
    
    total = user_data["cards_studied"]
    accuracy = (user_data["correct_answers"] / total * 100) if total > 0 else 0
    
    with col1:
        st.metric("Total Score", user_data["total_score"])
    with col2:
        st.metric("Cards Studied", total)
    with col3:
        st.metric("Accuracy", f"{accuracy:.1f}%")
    with col4:
        st.metric("Current Streak", user_data["current_streak"])


def leaderboard(users_list):
    """Display leaderboard"""
    st.subheader("🏆 Leaderboard")
    
    for idx, user in enumerate(users_list, 1):
        medal = "🥇" if idx == 1 else "🥈" if idx == 2 else "🥉" if idx == 3 else f"{idx}."
        st.write(f"{medal} **{user['_id']}** - {user['total_score']} points")