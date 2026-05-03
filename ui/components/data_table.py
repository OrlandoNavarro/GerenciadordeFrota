import streamlit as st
import pandas as pd


def render_table(rows: list[dict], columns: list[str] | None = None, entity: str | None = None):
    """Renderiza uma tabela no estilo planilha.

    Observações:
    - Não insere mais automaticamente a coluna "Editar" na planilha. O comportamento
      de edição deve ser tratado pelas páginas (por exemplo, com um `selectbox` abaixo
      da tabela ou via query params). Isso remove a coluna visual "Editar" da planilha.
    - Usa HTML+CSS para um layout mais agradável sobre a tabela (bordas, cabeçalho
      destacado e espaçamento).
    """
    if not rows:
        st.info('Nenhum registro encontrado')
        return

    df = pd.DataFrame(rows)
    if columns:
        # Reindex to the requested columns so missing columns are added as NaN
        df = df.reindex(columns=columns)

    # Render as HTML (keeps layout consistent across páginas)
    html_table = df.to_html(escape=False, index=False)

    css = (
        '<style>'
        '.st-table-wrapper {padding:8px; border:1px solid #e6e9ef; border-radius:8px; box-shadow:0 1px 2px rgba(0,0,0,0.03); background:#fff; overflow:auto;}'
        '.st-table-wrapper table {border-collapse: collapse; width:100%; font-family: inherit; table-layout: auto;}'
        '.st-table-wrapper thead th {background:#f6f7fb; font-weight:600; padding:10px; text-align:left; border-bottom:1px solid #eaeef3;}'
        '.st-table-wrapper tbody td {padding:10px; border-bottom:1px solid #f1f3f5;}'
        '.st-table-wrapper tbody tr:nth-child(even) {background:#fbfbfd;}'
        '.st-table-wrapper a {color:#0d6efd; text-decoration:none;}'
        '.st-table-wrapper a:hover {text-decoration:underline;}'
        '</style>'
    )

    st.markdown(f'<div class="st-table-wrapper">{css}{html_table}</div>', unsafe_allow_html=True)
