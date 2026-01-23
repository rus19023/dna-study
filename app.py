import streamlit as st

from core.state import init_state
from core.flashcard_logic import flip_card, next_card
from ui.layout import render_header
from ui.components import flashcard_box, controls

from data.deck_store import get_deck_names, get_deck, add_card


# ----------------------------
# Deck selection
# ----------------------------
deck_names = get_deck_names()

if not deck_names:
    st.error("No decks found in database.")
    st.stop()

deck_name = st.selectbox(
    "Choose a deck",
    options=deck_names
)

cards = get_deck(deck_name)


# ----------------------------
# Add new card (MongoDB-backed)
# ----------------------------
with st.expander("Add a new flashcard"):
    with st.form("add_card_form"):
        new_question = st.text_area("Question")
        new_answer = st.text_area("Answer")

        submitted = st.form_submit_button("Add card")

        if submitted:
            if not new_question.strip() or not new_answer.strip():
                st.error("Both question and answer are required.")
            else:
                add_card(
                    deck_name,
                    new_question.strip(),
                    new_answer.strip()
                )

                st.success("Flashcard added.")

                # Reset deck state so the new card appears
                st.session_state.pop("deck_id", None)
                st.experimental_rerun()


# ----------------------------
# Flashcard UI
# ----------------------------
init_state(cards)
render_header()

card = st.session_state.cards[st.session_state.index]
text = card["answer"] if st.session_state.show_answer else card["question"]

flashcard_box(text)

controls(
    on_flip=lambda: flip_card(st.session_state),
    on_next=lambda: next_card(st.session_state)
)

st.write(
    f"Card {st.session_state.index + 1} of {len(st.session_state.cards)}"
)
