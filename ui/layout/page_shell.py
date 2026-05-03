import streamlit as st
from ui.components.app_header import render_header
from ui.components.vertical_menu import render_menu
from ui.components.horizontal_toolbar import render_toolbar
from core.session import current_user, safe_rerun


def render_shell(content_callable):
    render_header()
    user = current_user()
    if not user:
        safe_rerun()
        return

    active = st.session_state.get('page', 'dashboard')

    # Layout with menu vertical na coluna esquerda e conteúdo à direita
    left_col, right_col = st.columns([1, 4])
    with left_col:
        render_menu(active)
    with right_col:
        # barra horizontal para ações rápidas (ex: ver todos os dados)
        render_toolbar()
        # Content area
        content_callable()
