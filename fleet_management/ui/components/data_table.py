import streamlit as st
import pandas as pd


def render_table(rows: list[dict], columns: list[str] | None = None):
    if not rows:
        st.info('Nenhum registro encontrado')
        return
    df = pd.DataFrame(rows)
    if columns:
        df = df[columns]
    st.dataframe(df)
