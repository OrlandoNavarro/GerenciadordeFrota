import streamlit as st
from config.theme import load_theme_css
from core.session import current_user, logout_user
from pathlib import Path
import os


def render_header():
    css = load_theme_css()
    if css:
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

    cols = st.columns([1, 6, 2])
    with cols[0]:
        # Resolve logo path relative to the package
        logo_path = Path(__file__).parent.parent.parent / 'assets' / 'logo' / 'logo.png'
        if logo_path.exists():
            st.image(str(logo_path), width=48)
        else:
            st.markdown('<div style="width:48px;height:48px;background:#eee;border-radius:8px"></div>', unsafe_allow_html=True)
    with cols[1]:
        st.markdown('<h3 style="margin:0;">Gerenciador de Frota</h3>', unsafe_allow_html=True)
    with cols[2]:
        user = current_user()
        if user:
            st.markdown(f"<div style='text-align:right;'>Olá, <b>{user.get('full_name') or user.get('email')}</b></div>", unsafe_allow_html=True)
            if st.button('Sair'):
                logout_user()
