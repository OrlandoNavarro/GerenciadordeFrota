# Fleet Management (Gerenciador de Frota)

Sistema básico de gestão de frotas e operações logísticas desenvolvido em Python + Streamlit.

Instalação rápida:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Criar e popular o banco (opcional):
# - método padrão (usa SQLAlchemy/repositórios):
python db/init_db.py
# - método alternativo (aplica db/schema.sql + db/seed.sql sem dependências externas):
python scripts/apply_seed_sqlite.py

# Executar a aplicação Streamlit (usando o venv):
./.venv/bin/streamlit run app.py --server.port 8501 --server.headless true --server.enableCORS false

# Logs locais (quando iniciado pelo helper):
# - streamlit.log
# - streamlit.err
```

Usuários de teste (criador automático): `admin@local` / `admin123`, `user@local` / `user123`.
