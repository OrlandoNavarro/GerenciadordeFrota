import streamlit as st
from core.navigation import get_menu_structure
from core.session import safe_rerun


def _toggle_expanded(key: str):
    st.session_state[key] = not st.session_state.get(key, False)


def render_menu(active: str | None = None):
    """Renderiza um menu vertical agrupado com submenus expansíveis.

    - `active`: chave da página ativa para destacar o item.
    """
    items = get_menu_structure()

    for idx, entry in enumerate(items):
        # item simples (link único)
        if "key" in entry:
            label = entry["label"]
            key = entry["key"]
            if key == active:
                st.markdown(f"**{label}**")
            else:
                if st.button(label, key=f"menu_{key}"):
                    st.session_state['page'] = key
                    safe_rerun()

        # item com subitens (seção) — torna-se expansível
        elif "items" in entry:
            toggle_key = f"menu_expanded_{idx}"
            # initialize if missing
            if toggle_key not in st.session_state:
                st.session_state[toggle_key] = False

            expanded = st.session_state.get(toggle_key, False)
            indicator = "▼ " if expanded else "► "

            # botão do cabeçalho da seção para alternar expansão
            if st.button(f"{indicator}{entry['label']}", key=f"menu_toggle_{idx}"):
                _toggle_expanded(toggle_key)
                safe_rerun()

            # mostrar subitens somente se expandido
            if st.session_state.get(toggle_key, False):
                for sub in entry["items"]:
                    sub_label = sub["label"]
                    sub_key = sub["key"]
                    if sub_key == active:
                        st.markdown(f"&nbsp;&nbsp;• **{sub_label}**", unsafe_allow_html=True)
                    else:
                        cols = st.columns([0.1, 1])
                        with cols[1]:
                            if st.button(sub_label, key=f"menu_item_{sub_key}"):
                                st.session_state['page'] = sub_key
                                safe_rerun()
