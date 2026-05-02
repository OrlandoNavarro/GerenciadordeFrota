import streamlit as st


def two_columns(left_callable, right_callable, left_ratio=2, right_ratio=1):
    cols = st.columns([left_ratio, right_ratio])
    with cols[0]:
        left_callable()
    with cols[1]:
        right_callable()
