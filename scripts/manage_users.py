#!/usr/bin/env python3
import sys, os
# Garantir que a raiz do projeto esteja no sys.path para imports relativos funcionarem
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import argparse
from config.database import SessionLocal
from domain.repositories.user_repository import UserRepository
from sqlalchemy import text


def list_users():
    db = SessionLocal()
    repo = UserRepository(db)
    users = repo.list()
    if not users:
        print('Nenhum usuário encontrado. Execute db/init_db.py para criar usuários padrão.')
        return
    for u in users:
        print(f"- {u.email} | {u.full_name or '-'} | role={u.role} | active={bool(u.is_active)}")
    db.close()


def set_password(email: str, password: str):
    db = SessionLocal()
    try:
        repo = UserRepository(db)
        user = repo.get_by_email(email)
        if not user:
            print(f"Usuário {email} não existe. Será criado com a senha fornecida.")
            try:
                repo.create_user({'email': email, 'full_name': email, 'password': password, 'role': 'admin'})
                db.commit()
                print('Usuário criado.')
            except Exception:
                db.rollback()
                db.execute(text("INSERT OR IGNORE INTO users (email, full_name, password_hash, role, is_active) VALUES (:email, :full_name, :password_hash, 'admin', 1)"),
                           {'email': email, 'full_name': email, 'password_hash': f'plain:{password}'})
                db.commit()
                print('Usuário criado (fallback plain).')
        else:
            try:
                from passlib.hash import bcrypt
                hashed = bcrypt.hash(password)
                user.password_hash = hashed
                db.commit()
                print('Senha atualizada.')
            except Exception:
                db.rollback()
                db.execute(text("UPDATE users SET password_hash = :pw WHERE email = :email"), {'pw': f'plain:{password}', 'email': email})
                db.commit()
                print('Senha atualizada (fallback plain).')
    finally:
        db.close()


def ensure_admin(email: str, password: str):
    db = SessionLocal()
    try:
        repo = UserRepository(db)
        if not repo.get_by_email(email):
            try:
                repo.create_user({'email': email, 'full_name': 'Administrador', 'password': password, 'role': 'admin'})
                db.commit()
                print('Admin criado.')
            except Exception:
                db.rollback()
                db.execute(text("INSERT OR IGNORE INTO users (email, full_name, password_hash, role, is_active) VALUES (:email, :full_name, :password_hash, 'admin', 1)"),
                           {'email': email, 'full_name': 'Administrador', 'password_hash': f'plain:{password}'})
                db.commit()
                print('Admin criado (fallback plain).')
        else:
            print('Admin já existe.')
    finally:
        db.close()


def main():
    parser = argparse.ArgumentParser(description='Gerenciar usuários do sistema')
    sub = parser.add_subparsers(dest='cmd')

    sub.add_parser('list', help='Listar usuários')

    sp_setpw = sub.add_parser('setpw', help='Setar senha para um usuário (cria se não existir)')
    sp_setpw.add_argument('email')
    sp_setpw.add_argument('password')

    sp_admin = sub.add_parser('ensure-admin', help='Criar admin se não existir')
    sp_admin.add_argument('--email', default='admin', help='E-mail do admin (padrão: admin)')
    sp_admin.add_argument('--password', default='admin', help='Senha do admin (padrão: admin)')

    args = parser.parse_args()
    if args.cmd == 'list':
        list_users()
    elif args.cmd == 'setpw':
        set_password(args.email, args.password)
    elif args.cmd == 'ensure-admin':
        ensure_admin(args.email, args.password)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
