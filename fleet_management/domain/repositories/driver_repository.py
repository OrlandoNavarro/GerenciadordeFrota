from domain.models.driver import Driver


class DriverRepository:
    def __init__(self, db_session):
        self.db = db_session

    def create(self, payload: dict) -> Driver:
        # basic create without duplicate checks for now
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

    def list(self, filters: dict | None = None):
        q = self.db.query(Driver)
        return q.all()
