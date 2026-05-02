import streamlit as st


def init_session():
    if 'user' not in st.session_state:
        st.session_state['user'] = None
    if 'page' not in st.session_state:
        st.session_state['page'] = 'login'
    if 'flash' not in st.session_state:
        st.session_state['flash'] = None


def login_user(user: dict):
    import streamlit as st
    st.session_state['user'] = user
    st.session_state['page'] = 'dashboard'


def logout_user():
    import streamlit as st
    st.session_state['user'] = None
    st.session_state['page'] = 'login'
    st.experimental_rerun()


def current_user():
    import streamlit as st
    return st.session_state.get('user')
