import sqlite3
from pathlib import Path
from config.settings import settings
from sqlalchemy import text
from config.database import engine
from domain.repositories.user_repository import UserRepository
from passlib.hash import bcrypt


ROOT = Path(__file__).parent


def _sqlite_path_from_url(url: str) -> Path:
    # expecting sqlite:///./fleet_management.db or sqlite:///fleet_management.db
    if url.startswith('sqlite:///'):
        path = url.replace('sqlite:///', '')
        return (Path.cwd() / path).resolve()
    return (Path.cwd() / 'fleet_management.db').resolve()


def init_db():
    db_path = _sqlite_path_from_url(settings.DATABASE_URL)
    db_dir = db_path.parent
    db_dir.mkdir(parents=True, exist_ok=True)

    schema_file = ROOT / 'schema.sql'
    seed_file = ROOT / 'seed.sql'

    if schema_file.exists():
        conn = sqlite3.connect(db_path)
        with open(schema_file, 'r', encoding='utf-8') as f:
            sql = f.read()
            conn.executescript(sql)
        if seed_file.exists():
            with open(seed_file, 'r', encoding='utf-8') as f:
                conn.executescript(f.read())
        conn.commit()
        conn.close()

    # Create admin users programmatically if not present
    with engine.connect() as connection:
        try:
            res = connection.execute(text("SELECT COUNT(*) FROM users"))
            count = res.scalar_one()
        except Exception:
            count = 0

    from sqlalchemy.orm import Session
    session = Session(bind=engine)
    user_repo = UserRepository(session)
    if not user_repo.get_by_email('admin@local'):
        user_repo.create_user({
            'email': 'admin@local',
            'full_name': 'Administrador',
            'password': 'admin123',
            'role': 'admin',
        })
    # Also create a simple test user 'admin' with password 'admin' for quick access
    if not user_repo.get_by_email('admin'):
        user_repo.create_user({
            'email': 'admin',
            'full_name': 'Administrador Teste',
            'password': 'admin',
            'role': 'admin',
        })
    if not user_repo.get_by_email('user@local'):
        user_repo.create_user({
            'email': 'user@local',
            'full_name': 'Usuário',
            'password': 'user123',
            'role': 'operador',
        })
    session.commit()
    session.close()


if __name__ == '__main__':
    init_db()
