import streamlit as st
import random


def init_state(cards):
    deck_id = id(cards)

    if st.session_state.get("deck_id") != deck_id:
        st.session_state.deck_id = deck_id
        st.session_state.cards = list(cards)
        random.shuffle(st.session_state.cards)
        st.session_state.index = 0
        st.session_state.show_answer = False


