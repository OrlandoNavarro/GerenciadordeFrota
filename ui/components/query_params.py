import streamlit as st
from typing import Dict, List, Any


def get_query_params() -> Dict[str, List[str]]:
    """Retorna os query params da URL de forma compatível entre versões do Streamlit.

    Retorna um dicionário onde cada valor é uma lista de strings, semelhante
    ao comportamento de `st.experimental_get_query_params()` nas versões antigas.
    """
    # Prefer experimental API se disponível
    if hasattr(st, 'experimental_get_query_params'):
        try:
            return st.experimental_get_query_params() or {}
        except Exception:
            pass

    # Nova API: st.query_params (proxy)
    if hasattr(st, 'query_params'):
        try:
            qp = st.query_params
            # qp pode ser um Mapping[str, Union[str, List[str]]]
            out: Dict[str, List[str]] = {}
            for k, v in dict(qp).items():
                if v is None:
                    out[k] = []
                elif isinstance(v, list):
                    out[k] = [str(x) for x in v]
                else:
                    out[k] = [str(v)]
            return out
        except Exception:
            pass

    # Fallback: nenhum query param disponível
    return {}
