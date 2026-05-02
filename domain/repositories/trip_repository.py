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

    def list(self, filters: dict | None = None):
        q = self.db.query(Trip)
        return q.all()
