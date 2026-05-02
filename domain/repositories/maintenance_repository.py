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

    def get(self, id: int):
        return self.db.query(Maintenance).filter(Maintenance.id == id).first()

    def list(self, filters: dict | None = None):
        q = self.db.query(Maintenance)
        if filters:
            if 'vehicle_id' in filters and filters['vehicle_id'] is not None:
                q = q.filter(Maintenance.vehicle_id == filters['vehicle_id'])
            if 'tipo' in filters and filters['tipo']:
                q = q.filter(Maintenance.tipo.ilike(f"%{filters['tipo']}%"))
            if 'status' in filters and filters['status']:
                q = q.filter(Maintenance.status == filters['status'])
            if 'date_from' in filters and filters['date_from']:
                q = q.filter(Maintenance.data >= filters['date_from'])
            if 'date_to' in filters and filters['date_to']:
                q = q.filter(Maintenance.data <= filters['date_to'])
        return q.order_by(Maintenance.id.desc()).all()

    def update(self, id: int, payload: dict):
        m = self.get(id)
        if not m:
            return None
        for k, val in payload.items():
            if hasattr(m, k) and k != 'id':
                setattr(m, k, val)
        self.db.flush()
        return m

    def delete(self, id: int):
        m = self.get(id)
        if not m:
            return False
        # mark as cancelled
        m.status = 'cancelado'
        self.db.flush()
        return True
