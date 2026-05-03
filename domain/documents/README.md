# Módulo Documentos

Este documento descreve a estrutura inicial do módulo de `Documentos`.

Localização dos componentes:

- Modelo: `domain/models/document.py`
- Repositório: `domain/repositories/document_repository.py`
- Serviço: `domain/services/document_service.py`
- Página UI: `ui/pages/documents_page.py`

Modelo (campos principais):

- `id` (Integer, PK)
- `tipo_documento` (String)
- `categoria_referencia` (String) — categoria do item relacionado (ex: `vehicle`, `driver`, `trip`, `transporter`)
- `referencia_id` (Integer) — id do registro relacionado na categoria indicada
- `numero` (String)
- `data_emissao` (Date)
- `data_vencimento` (Date)
- `status` (String) — exemplos: `vigente`, `vencido`, `cancelado`
- `observacoes` (Text)

Repositório (`DocumentRepository`):

- `create(payload)` — cria um documento e retorna a instância
- `get(id)` — retorna um documento por id
- `list(filters)` — lista documentos com filtros opcionais (tipo, número, status, categoria, referência, intervalo de datas)
- `update(id, payload)` — atualiza campos do documento
- `delete(id)` — marca documento como `cancelado`

Serviço (`DocumentService`): camada fina que delega para o repositório com os métodos:

- `create_document(payload)`
- `list_documents(filters)`
- `get_document(id)`
- `update_document(id, payload)`
- `delete_document(id)`

UI (`ui/pages/documents_page.py`):

- Aba `Cadastro`: formulário para novo documento ou para edição quando `edit_document` estiver presente nos query params.
- Aba `Listagem`: filtros, paginação, tabela e formulário de edição selecionável abaixo da tabela.
- Aba `Indicadores`: métricas simples (total, vigentes).

Exemplo de payload para criação/atualização:

```py
payload = {
    'tipo_documento': 'CRLV',
    'categoria_referencia': 'vehicle',
    'referencia_id': 12,
    'numero': '12345',
    'data_emissao': date(2024, 1, 1),
    'data_vencimento': date(2026, 1, 1),
    'status': 'vigente',
    'observacoes': 'Documento digitalizado no sistema.'
}
```

Próximos passos sugeridos:

- Adicionar testes unitários para repositório/serviço.
- Melhorar seleção de referência (ex: autocompletar por categoria ao invés de ID livre).
- Internacionalização / validações de campos.
