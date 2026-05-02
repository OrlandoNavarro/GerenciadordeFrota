from typing import List, Tuple


def get_menu_items() -> List[Tuple[str, str]]:
    return [
        ("Dashboard", "dashboard"),
        ("Transportadoras", "transporters"),
        ("Veículos", "vehicles"),
        ("Motoristas", "drivers"),
        ("Viagens", "trips"),
        ("Abastecimentos", "fuelings"),
        ("Manutenções", "maintenances"),
        ("Documentos", "documents"),
        ("Relatórios", "reports"),
        ("Configurações", "settings"),
    ]
