from domain.repositories.fueling_repository import FuelingRepository


class FuelingService:
    def __init__(self, db_session):
        self.db = db_session
        self.repo = FuelingRepository(db_session)

    def create_fueling(self, payload: dict):
        # compute valor_por_litro if missing
        if payload.get('litros') and payload.get('valor_total') and not payload.get('valor_por_litro'):
            payload['valor_por_litro'] = payload['valor_total'] / max(1, payload['litros'])
        return self.repo.create(payload)
    
    def list_fuelings(self, filters: dict | None = None):
        return self.repo.list(filters)

    def get_fueling(self, id: int):
        return self.repo.get(id)

    def update_fueling(self, id: int, payload: dict):
        if payload.get('litros') and payload.get('valor_total') and not payload.get('valor_por_litro'):
            payload['valor_por_litro'] = payload['valor_total'] / max(1, payload['litros'])
        return self.repo.update(id, payload)

    def delete_fueling(self, id: int):
        return self.repo.delete(id)
