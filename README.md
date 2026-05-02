# Fleet Management (Gerenciador de Frota)

Sistema básico de gestão de frotas e operações logísticas desenvolvido em Python + Streamlit.

Instalação rápida:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r fleet_management/requirements.txt
cp fleet_management/.env.example .env
python fleet_management/db/init_db.py
streamlit run fleet_management/app.py
```

Usuários de teste (criador automático): `admin@local` / `admin123`, `user@local` / `user123`.
