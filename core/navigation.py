from typing import List, Tuple, Dict, Any


def get_menu_structure() -> List[Dict[str, Any]]:
    """Retorna a estrutura do menu organizada em seções com possíveis subitens.

    Estrutura esperada:
    [
        {"label": "Dashboard", "key": "dashboard"},
        {"label": "Cadastro", "items": [{"label": "Transportadoras", "key": "transporters"}, ...]},
        ...
    ]
    """
    return [
        {"label": "Dashboard", "key": "dashboard"},
        {"label": "Cadastro", "items": [
            {"label": "Transportadoras", "key": "transporters"},
            {"label": "Motoristas", "key": "drivers"},
            {"label": "Veículos", "key": "vehicles"},
        ]},
        {"label": "Operações", "items": [
            {"label": "Viagens", "key": "trips"},
            {"label": "Abastecimentos", "key": "fuelings"},
            {"label": "Manutenções", "key": "maintenances"},
        ]},
        {"label": "Relatórios", "items": [
            {"label": "Documentos", "key": "documents"},
            {"label": "Relatórios", "key": "reports"},
            {"label": "Configurações", "key": "settings"},
        ]},
    ]


def get_menu_items() -> List[Tuple[str, str]]:
    """Compatibilidade: retorna lista plana (label, key) de todos os itens do menu."""
    items: List[Tuple[str, str]] = []
    for entry in get_menu_structure():
        if "key" in entry:
            items.append((entry["label"], entry["key"]))
        elif "items" in entry:
            for sub in entry["items"]:
                items.append((sub["label"], sub["key"]))
    return items
