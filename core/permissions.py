from enum import Enum


class Role(str, Enum):
    ADMIN = 'admin'
    GESTOR = 'gestor'
    OPERADOR = 'operador'
    CONSULTA = 'consulta'


def has_role(user: dict | None, allowed: list[str]) -> bool:
    if not user:
        return False
    return user.get('role') in allowed
