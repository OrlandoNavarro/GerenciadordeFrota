from domain.models.vehicle import Vehicle


class VehicleRepository:
    def __init__(self, db_session):
        self.db = db_session

    def create(self, payload: dict) -> Vehicle:
        existing = self.get_by_plate(payload.get('placa'))
        if existing:
            raise ValueError('Placa já existe')
        v = Vehicle(
            placa=payload.get('placa'),
            tipo=payload.get('tipo'),
            modelo=payload.get('modelo'),
            marca=payload.get('marca'),
            ano=payload.get('ano'),
            capacidade=payload.get('capacidade'),
            combustivel=payload.get('combustivel'),
            consumo_medio=payload.get('consumo_medio'),
            status=payload.get('status', 'ativo'),
            transporter_id=payload.get('transporter_id'),
            observacoes=payload.get('observacoes'),
        )
        self.db.add(v)
        self.db.flush()
        return v

    def get_by_plate(self, placa: str):
        return self.db.query(Vehicle).filter(Vehicle.placa == placa).first()

    def get(self, id: int):
        return self.db.query(Vehicle).filter(Vehicle.id == id).first()

    def list(self, filters: dict | None = None):
        q = self.db.query(Vehicle)
        if filters:
            if 'placa' in filters:
                q = q.filter(Vehicle.placa.ilike(f"%{filters['placa']}%"))
            if 'transporter_id' in filters:
                q = q.filter(Vehicle.transporter_id == filters['transporter_id'])
            if 'status' in filters:
                q = q.filter(Vehicle.status == filters['status'])
        return q.order_by(Vehicle.id.desc()).all()

    def update(self, id: int, payload: dict):
        v = self.get(id)
        if not v:
            return None
        if 'placa' in payload:
            existing = self.get_by_plate(payload['placa'])
            if existing and existing.id != id:
                raise ValueError('Placa já existe')
        for k, val in payload.items():
            if hasattr(v, k) and k != 'id':
                setattr(v, k, val)
        self.db.flush()
        return v

    def delete(self, id: int):
        v = self.get(id)
        if not v:
            return False
        v.status = 'inativo'
        self.db.flush()
        return True
