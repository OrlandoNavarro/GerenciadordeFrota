import re


def sanitize_cnpj(cnpj: str) -> str:
    return re.sub(r"\D", "", cnpj or "")


def sanitize_cpf(cpf: str) -> str:
    return re.sub(r"\D", "", cpf or "")
