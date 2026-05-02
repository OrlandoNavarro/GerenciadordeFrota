import streamlit as st
import pandas as pd


def render_table(rows: list[dict], columns: list[str] | None = None, entity: str | None = None):
    """Renderiza uma tabela no estilo planilha. Se `entity` for fornecido e a coluna
    `id` estiver presente, substitui a coluna `id` por uma coluna `Editar` com um
    link/ícone que adiciona um parâmetro de query `edit_<entity>=<id>` na URL.

    Observação: manter o layout o mais próximo possível do `st.dataframe`, mas usar
    HTML para permitir links clicáveis por linha.
    """
    if not rows:
        st.info('Nenhum registro encontrado')
        return

    df = pd.DataFrame(rows)
    if columns:
        # Reindex to the requested columns so missing columns are added as NaN
        # (avoids KeyError when some rows don't include every key)
        df = df.reindex(columns=columns)

    # If entity provided and id column exists, render HTML table with Edit links
    if entity and 'id' in df.columns:
        # build edit column with anchor links that set a query param
        try:
            edit_col = df['id'].apply(lambda x: f'<a href="?edit_{entity}={x}" style="text-decoration:none;color:#000;">✎</a>')
        except Exception:
            edit_col = df['id'].apply(lambda x: '✎')

        cols = list(df.columns)
        id_index = cols.index('id')

        df2 = df.copy()
        # insert 'Editar' at the id position then drop original id
        df2.insert(id_index, 'Editar', edit_col)
        df2 = df2.drop(columns=['id'])

        # Render as HTML preserving the cell layout and allowing the link
        html_table = df2.to_html(escape=False, index=False)

        css = (
            '<style>'
            '.st-table-wrapper table {border-collapse: collapse; width:100%; font-family: inherit;}'
            '.st-table-wrapper th, .st-table-wrapper td {padding:8px; border-bottom:1px solid #eee; text-align:left;}'
            '.st-table-wrapper tr:nth-child(even) {background:#fafafa;}'
            '.st-table-wrapper a {color: #000;}'
            '</style>'
        )

        st.markdown(f'<div class="st-table-wrapper">{css}{html_table}</div>', unsafe_allow_html=True)
    else:
        # fallback to the dataframe view (keeps look & feel)
        st.dataframe(df)
