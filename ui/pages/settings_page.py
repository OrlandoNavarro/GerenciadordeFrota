import streamlit as st
from config.database import SessionLocal
from domain.services.user_service import UserService
from core.session import current_user, login_user
from ui.components.form_section import section
from core.navigation import get_menu_items


def _get_user_id(user_obj):
    if user_obj is None:
        return None
    if isinstance(user_obj, dict):
        return user_obj.get('id')
    return getattr(user_obj, 'id', None)


def render():
    st.title('Configurações')
    tabs = st.tabs(['Perfil', 'Preferências'])

    db = SessionLocal()
    usvc = UserService(db)

    user_obj = current_user()
    user_id = _get_user_id(user_obj)
    profile = None
    if user_id:
        try:
            profile = usvc.get_user(user_id)
        except Exception:
            profile = None

    with tabs[0]:
        section('Perfil de usuário')
        if not profile:
            st.info('Nenhum usuário logado ou perfil não encontrado.')
        else:
            with st.form('profile_form'):
                full_name = st.text_input('Nome completo', value=profile.full_name or '')
                email = st.text_input('E-mail', value=profile.email or '')
                new_password = st.text_input('Nova senha (opcional)', type='password')
                confirm_password = st.text_input('Confirmar nova senha', type='password')
                updated = st.form_submit_button('Salvar perfil')
                if updated:
                    if new_password and new_password != confirm_password:
                        st.error('As senhas não conferem')
                    else:
                        payload = {
                            'full_name': full_name,
                            'email': email,
                        }
                        if new_password:
                            payload['password'] = new_password
                        try:
                            usvc.update_user(profile.id, payload)
                            db.commit()
                            st.success('Perfil atualizado')
                            # atualizar sessão se contiver dados do usuário
                            try:
                                if isinstance(user_obj, dict):
                                    user_obj.update({'full_name': full_name, 'email': email})
                                    login_user(user_obj)
                            except Exception:
                                pass
                        except Exception as e:
                            db.rollback()
                            st.error(str(e))

    with tabs[1]:
        section('Preferências')
        prefs = st.session_state.get('preferences', {}) or {}
        menu_items = [label for label, key in get_menu_items()]
        with st.form('prefs_form'):
            default_page = st.selectbox('Página padrão', options=['dashboard'] + menu_items, index=0)
            theme = st.selectbox('Tema', ['Light', 'Dark'], index=0 if prefs.get('theme', 'Light') == 'Light' else 1)
            items_per_page = st.number_input('Itens por página', min_value=5, max_value=100, value=prefs.get('items_per_page', 10))
            saved = st.form_submit_button('Salvar preferências')
            if saved:
                st.session_state['preferences'] = {
                    'default_page': default_page,
                    'theme': theme,
                    'items_per_page': int(items_per_page),
                }
                st.success('Preferências salvas (temporárias na sessão)')
