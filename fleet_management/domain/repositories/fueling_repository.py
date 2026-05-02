from domain.models.fueling import Fueling


class FuelingRepository:
    def __init__(self, db_session):
        self.db = db_session

    def create(self, payload: dict) -> Fueling:
        f = Fueling(
            data=payload.get('data'),
            vehicle_id=payload.get('vehicle_id'),
            motorista_id=payload.get('motorista_id'),
            posto=payload.get('posto'),
            litros=payload.get('litros'),
            valor_total=payload.get('valor_total'),
            valor_por_litro=payload.get('valor_por_litro'),
            km_atual=payload.get('km_atual'),
            observacoes=payload.get('observacoes'),
        )
        self.db.add(f)
        self.db.flush()
        return f

    def list(self, filters: dict | None = None):
        q = self.db.query(Fueling)
        return q.all()
