import streamlit as st


def render_empty(title: str, subtitle: str = ''):
    st.markdown(f"<div style='text-align:center;padding:28px' class='card'><h3>{title}</h3><div style='color:#6b6b6b'>{subtitle}</div></div>", unsafe_allow_html=True)
