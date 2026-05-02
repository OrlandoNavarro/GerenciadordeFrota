from domain.models.maintenance import Maintenance


class MaintenanceRepository:
    def __init__(self, db_session):
        self.db = db_session

    def create(self, payload: dict) -> Maintenance:
        m = Maintenance(
            vehicle_id=payload.get('vehicle_id'),
            tipo=payload.get('tipo'),
            data=payload.get('data'),
            oficina=payload.get('oficina'),
            custo=payload.get('custo'),
            descricao=payload.get('descricao'),
            status=payload.get('status', 'aberto'),
            proxima_revisao=payload.get('proxima_revisao'),
            observacoes=payload.get('observacoes'),
        )
        self.db.add(m)
        self.db.flush()
        return m

    def list(self, filters: dict | None = None):
        q = self.db.query(Maintenance)
        return q.all()
