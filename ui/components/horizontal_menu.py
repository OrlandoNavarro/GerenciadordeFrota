import streamlit as st
from core.navigation import get_menu_items


def render_menu(active: str | None = None):
    items = get_menu_items()
    cols = st.columns(len(items))
    for i, (label, key) in enumerate(items):
        style = "font-weight:600; color: #6750A4;" if key == active else "color: #333;"
        with cols[i]:
            if st.button(label):
                st.session_state['page'] = key
                st.experimental_rerun()
