import streamlit as st


def stat_card(title: str, value, delta: str | None = None):
    st.markdown(f"<div class='card kpi'><div style='font-size:12px;color:#6b6b6b'>{title}</div><div style='font-size:20px;font-weight:700'>{value}</div>{f'<div style=\'font-size:12px;color:#2e7d32\'>{delta}</div>' if delta else ''}</div>", unsafe_allow_html=True)
