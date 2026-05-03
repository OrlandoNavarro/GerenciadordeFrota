# Módulo Relatórios

Estrutura inicial do módulo de Relatórios.

Objetivo:
- Fornecer páginas para geração de relatórios com filtros e opções de exportação (CSV/JSON).
- Agregar indicadores e visualizações resumidas por entidade.

Localização:
- Página UI: `ui/pages/reports_page.py`

Comportamento atual:
- Aba `Gerar`: permite selecionar a entidade, aplicar filtros simples (texto, intervalo de datas, status) e gerar resultados.
- Exportação: CSV e JSON a partir dos resultados filtrados.
- Aba `Exportações`: explicativa; podem ser adicionadas exportações agendadas e histórico.
- Aba `Indicadores`: placeholder para futuros gráficos/resumos.

Próximos passos sugeridos:
- Suporte a Excel (`.xlsx`) usando `openpyxl`/`xlsxwriter`.
- Relatórios agendados e download em lote.
- Melhor mapeamento de filtros por entidade (autocomplete, seleção de referência).
