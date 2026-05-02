import streamlit as st


def card(title: str, body_callable):
    st.markdown(f"<div class='card'><h4>{title}</h4>", unsafe_allow_html=True)
    body_callable()
    st.markdown('</div>', unsafe_allow_html=True)
