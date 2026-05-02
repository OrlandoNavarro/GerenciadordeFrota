from domain.models.trip import Trip


class TripRepository:
    def __init__(self, db_session):
        self.db = db_session

    def create(self, payload: dict) -> Trip:
        t = Trip(
            origem=payload.get('origem'),
            destino=payload.get('destino'),
            data_saida=payload.get('data_saida'),
            data_prevista_chegada=payload.get('data_prevista_chegada'),
            data_chegada=payload.get('data_chegada'),
            motorista_id=payload.get('motorista_id'),
            vehicle_id=payload.get('vehicle_id'),
            transporter_id=payload.get('transporter_id'),
            tipo_carga=payload.get('tipo_carga'),
            peso=payload.get('peso'),
            custo=payload.get('custo'),
            status=payload.get('status', 'planejada'),
            observacoes=payload.get('observacoes'),
        )
        self.db.add(t)
        self.db.flush()
        return t

    def get(self, id: int):
        return self.db.query(Trip).filter(Trip.id == id).first()

    def list(self, filters: dict | None = None):
        q = self.db.query(Trip)
        if filters:
            if 'origem' in filters:
                q = q.filter(Trip.origem.ilike(f"%{filters['origem']}%"))
            if 'destino' in filters:
                q = q.filter(Trip.destino.ilike(f"%{filters['destino']}%"))
            if 'transporter_id' in filters:
                q = q.filter(Trip.transporter_id == filters['transporter_id'])
            if 'status' in filters:
                q = q.filter(Trip.status == filters['status'])
        return q.order_by(Trip.id.desc()).all()

    def update(self, id: int, payload: dict):
        t = self.get(id)
        if not t:
            return None
        for k, val in payload.items():
            if hasattr(t, k) and k != 'id':
                setattr(t, k, val)
        self.db.flush()
        return t

    def delete(self, id: int):
        t = self.get(id)
        if not t:
            return False
        # mark trip as cancelled
        t.status = 'cancelada'
        self.db.flush()
        return True
