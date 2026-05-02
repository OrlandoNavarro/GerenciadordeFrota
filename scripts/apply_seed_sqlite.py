#!/usr/bin/env python3
import sqlite3
from pathlib import Path
import os


def _sqlite_path_from_url(url: str) -> Path:
    if url.startswith('sqlite:///'):
        path = url.replace('sqlite:///', '')
        return (Path.cwd() / path).resolve()
    return (Path.cwd() / 'fleet_management.db').resolve()


def main():
    db_url = os.getenv('DATABASE_URL', 'sqlite:///./fleet_management.db')
    db_path = _sqlite_path_from_url(db_url)
    db_path.parent.mkdir(parents=True, exist_ok=True)

    root = Path(__file__).resolve().parent.parent
    schema_file = root / 'db' / 'schema.sql'
    seed_file = root / 'db' / 'seed.sql'

    if not schema_file.exists():
        print('Esquema não encontrado:', schema_file)
        return

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # Limpar dados existentes nas tabelas alvo para evitar conflitos de FK
    try:
        cur.execute('PRAGMA foreign_keys = OFF')
        for t in ('maintenances', 'fuelings', 'trips', 'vehicles', 'drivers', 'transporters'):
            try:
                cur.execute(f'DELETE FROM {t}')
            except Exception:
                pass
        conn.commit()
    finally:
        cur.execute('PRAGMA foreign_keys = ON')

    # Aplicar esquema (cria tabelas se necessário)
    with open(schema_file, 'r', encoding='utf-8') as f:
        sql = f.read()
        conn.executescript(sql)

    # Aplicar seed
    if seed_file.exists():
        with open(seed_file, 'r', encoding='utf-8') as f:
            conn.executescript(f.read())

    conn.commit()
    conn.close()
    print(f'Schema e seed aplicados em: {db_path}')


if __name__ == '__main__':
    main()
