import streamlit as st
import pandas as pd


def render_table(rows: list[dict], columns: list[str] | None = None):
    if not rows:
        st.info('Nenhum registro encontrado')
        return
    df = pd.DataFrame(rows)
    if columns:
        # Reindex to the requested columns so missing columns are added as NaN
        # (avoids KeyError when some rows don't include every key)
        df = df.reindex(columns=columns)
    st.dataframe(df)
