import streamlit as st
from config.database import SessionLocal
from domain.services.user_service import UserService
from core.session import login_user, safe_rerun


def render():
    st.set_page_config(page_title='Login - Gerenciador de Frota')
    st.markdown('<div style="display:flex;justify-content:center;align-items:center;height:70vh">', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="card" style="max-width:420px;margin:0 auto;padding:24px">', unsafe_allow_html=True)
        st.markdown('<h3 style="text-align:center;margin-bottom:8px">Entrar</h3>', unsafe_allow_html=True)
        email = st.text_input('E-mail')
        password = st.text_input('Senha', type='password')
        remember = st.checkbox('Lembrar acesso')
        st.write('</div>', unsafe_allow_html=True)

        if st.button('Entrar'):
            if not email or not password:
                st.error('Preencha email e senha')
            else:
                db = SessionLocal()
                service = UserService(db)
                user = service.authenticate(email, password)
                if not user:
                    st.error('Credenciais inválidas')
                else:
                    login_user(user.to_dict())
                    st.success('Login efetuado com sucesso')
                    safe_rerun()
