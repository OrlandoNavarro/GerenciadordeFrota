from domain.models.driver import Driver


class DriverRepository:
    def __init__(self, db_session):
        self.db = db_session

    def create(self, payload: dict) -> Driver:
        existing = self.get_by_cpf(payload.get('cpf'))
        if existing:
            raise ValueError('CPF já cadastrado')
        d = Driver(
            nome=payload.get('nome'),
            cpf=payload.get('cpf'),
            cnh=payload.get('cnh'),
            categoria=payload.get('categoria'),
            validade_cnh=payload.get('validade_cnh'),
            telefone=payload.get('telefone'),
            email=payload.get('email'),
            transporter_id=payload.get('transporter_id'),
            status=payload.get('status', 'ativo'),
            observacoes=payload.get('observacoes'),
        )
        self.db.add(d)
        self.db.flush()
        return d

    def get(self, id: int):
        return self.db.query(Driver).filter(Driver.id == id).first()

    def get_by_cpf(self, cpf: str):
        return self.db.query(Driver).filter(Driver.cpf == cpf).first()

    def list(self, filters: dict | None = None):
        q = self.db.query(Driver)
        if filters:
            if 'nome' in filters:
                q = q.filter(Driver.nome.ilike(f"%{filters['nome']}%"))
            if 'cpf' in filters:
                q = q.filter(Driver.cpf == filters['cpf'])
            if 'status' in filters:
                q = q.filter(Driver.status == filters['status'])
        return q.order_by(Driver.id.desc()).all()

    def update(self, id: int, payload: dict):
        d = self.get(id)
        if not d:
            return None
        if 'cpf' in payload:
            existing = self.get_by_cpf(payload['cpf'])
            if existing and existing.id != id:
                raise ValueError('CPF já cadastrado')
        for k, v in payload.items():
            if hasattr(d, k) and k != 'id':
                setattr(d, k, v)
        self.db.flush()
        return d

    def delete(self, id: int):
        d = self.get(id)
        if not d:
            return False
        d.status = 'inativo'
        self.db.flush()
        return True
