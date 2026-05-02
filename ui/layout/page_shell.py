import streamlit as st
from ui.components.app_header import render_header
from ui.components.horizontal_menu import render_menu
from core.session import current_user


def render_shell(content_callable):
    render_header()
    user = current_user()
    if not user:
        st.experimental_rerun()
        return

    st.markdown('---')
    # Render horizontal menu
    active = st.session_state.get('page', 'dashboard')
    render_menu(active)
    st.markdown('---')

    # Content area
    content_callable()
