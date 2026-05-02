import streamlit as st


def render_filters(filters: dict):
    cols = st.columns(len(filters))
    keys = list(filters.keys())
    for i, k in enumerate(keys):
        with cols[i]:
            filters[k] = st.text_input(k, value=filters.get(k) or '')
    return filters
