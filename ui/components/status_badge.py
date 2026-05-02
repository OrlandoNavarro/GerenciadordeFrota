import streamlit as st


def badge(text: str, kind: str = 'info'):
    colors = {
        'info': '#0288D1',
        'success': '#2E7D32',
        'warning': '#ED6C02',
        'error': '#B3261E'
    }
    color = colors.get(kind, '#0288D1')
    st.markdown(f"<span style='background:{color}; color:#fff; padding:6px 10px; border-radius:999px; font-size:12px'>{text}</span>", unsafe_allow_html=True)
