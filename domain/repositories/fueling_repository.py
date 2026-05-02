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

    def get(self, id: int):
        return self.db.query(Fueling).filter(Fueling.id == id).first()

    def list(self, filters: dict | None = None):
        q = self.db.query(Fueling)
        if filters:
            if 'vehicle_id' in filters and filters['vehicle_id'] is not None:
                q = q.filter(Fueling.vehicle_id == filters['vehicle_id'])
            if 'motorista_id' in filters and filters['motorista_id'] is not None:
                q = q.filter(Fueling.motorista_id == filters['motorista_id'])
            if 'posto' in filters and filters['posto']:
                q = q.filter(Fueling.posto.ilike(f"%{filters['posto']}%"))
            if 'date_from' in filters and filters['date_from']:
                q = q.filter(Fueling.data >= filters['date_from'])
            if 'date_to' in filters and filters['date_to']:
                q = q.filter(Fueling.data <= filters['date_to'])
        return q.order_by(Fueling.id.desc()).all()

    def update(self, id: int, payload: dict):
        f = self.get(id)
        if not f:
            return None
        for k, val in payload.items():
            if hasattr(f, k) and k != 'id':
                setattr(f, k, val)
        self.db.flush()
        return f

    def delete(self, id: int):
        f = self.get(id)
        if not f:
            return False
        self.db.delete(f)
        self.db.flush()
        return True
