#!/usr/bin/env python3
import sqlite3
from pathlib import Path
from config.settings import settings


def _sqlite_path_from_url(url: str) -> Path:
    if url.startswith('sqlite:///'):
        return Path(url.replace('sqlite:///', '')).resolve()
    return (Path.cwd() / 'fleet_management.db').resolve()


def main():
    db_path = _sqlite_path_from_url(settings.DATABASE_URL)
    if not db_path.exists():
        print(f'Arquivo de banco não encontrado: {db_path}')
        return

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # Verificar se a tabela trips existe
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='trips'")
    if not cur.fetchone():
        print('Tabela `trips` não encontrada no banco. Verifique o schema.')
        conn.close()
        return

    # Obter colunas atuais
    cur.execute("PRAGMA table_info(trips)")
    cols = [r[1] for r in cur.fetchall()]

    if 'valor_frete' in cols:
        print('Coluna `valor_frete` já existe. Nada a fazer.')
    else:
        # Adicionar coluna
        print('Adicionando coluna `valor_frete`...')
        cur.execute('ALTER TABLE trips ADD COLUMN valor_frete REAL')

        # Se existir coluna `custo`, copiar valores para `valor_frete`
        if 'custo' in cols:
            print('Coluna `custo` encontrada — copiando valores para `valor_frete`...')
            try:
                cur.execute('UPDATE trips SET valor_frete = custo WHERE valor_frete IS NULL')
            except Exception as e:
                print('Falha ao copiar valores de custo:', e)

        conn.commit()
        print('Migração concluída com sucesso.')

    conn.close()


if __name__ == '__main__':
    main()
