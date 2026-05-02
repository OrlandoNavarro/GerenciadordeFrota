import streamlit as st


def section(title: str):
    st.markdown(f"<h4 style='margin:8px 0'>{title}</h4>", unsafe_allow_html=True)
