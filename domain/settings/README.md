# Módulo Configurações

Estrutura inicial das configurações do sistema.

Objetivos:
- Permitir edição do perfil do usuário (nome, e-mail, senha).
- Fornecer preferências de usuário (tema, página padrão, itens por página).

Localização:
- Página UI: `ui/pages/settings_page.py`
- Serviço/Modelo: `domain/services/user_service.py`, `domain/models/user.py`

Comportamento atual:
- Aba `Perfil`: formulário para atualizar `full_name`, `email` e senha. Persiste via `UserService.update_user`.
- Aba `Preferências`: salva preferências temporariamente em `st.session_state['preferences']`.

Próximos passos sugeridos:
- Persistir preferências por usuário no banco de dados (nova tabela `user_preferences`).
- Painel de administração para gerenciar roles e permissões.
- Validações e verificações de segurança (requer senha atual para alterar e-mail/senha).
