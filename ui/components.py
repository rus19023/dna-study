import streamlit as st


def flashcard_box(text):
    st.markdown(
        f"""
        <div style="
            font-size:24px;
            padding:20px;
            border-radius:10px;
            border:2px solid #ddd;
            text-align:center;">
            {text}
        </div>
        """,
        unsafe_allow_html=True
    )
    

def controls(on_flip, on_next):
    col1, col2 = st.columns(2)
    with col1:
        st.button("🔄 Flip", on_click=on_flip)
    with col2:
        st.button("➡️ Next", on_click=on_next)
