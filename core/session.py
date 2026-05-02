import time
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


def safe_rerun():
    """Trigger a rerun de forma compatível com múltiplas versões do Streamlit.

    Tenta chamar `st.experimental_rerun()` quando disponível. Se não estiver,
    altera os query params via `st.experimental_set_query_params` como fallback.
    Se nada funcionar, marca uma flag em `st.session_state` para indicar
    que uma rerun foi solicitada (mínimo esforço para evitar exceções).
    """
    try:
        st.experimental_rerun()
        return
    except Exception:
        try:
            # Forçar uma mudança de query params para acionar rerun em versões
            # onde experimental_rerun não existe.
            st.experimental_set_query_params(_r=int(time.time()))
            return
        except Exception:
            # último recurso: setar flag na session_state
            try:
                st.session_state['_rerun_requested'] = True
            except Exception:
                pass


def logout_user():
    import streamlit as st
    st.session_state['user'] = None
    st.session_state['page'] = 'login'
    safe_rerun()


def current_user():
    import streamlit as st
    return st.session_state.get('user')
