from domain.models.transporter import Transporter


class TransporterRepository:
    def __init__(self, db_session):
        self.db = db_session

    def create(self, payload: dict) -> Transporter:
        exists = self.get_by_cnpj(payload.get('cnpj'))
        if exists:
            raise ValueError('CNPJ já cadastrado')
        tr = Transporter(
            razao_social=payload.get('razao_social'),
            nome_fantasia=payload.get('nome_fantasia'),
            cnpj=payload.get('cnpj'),
            inscricao_estadual=payload.get('inscricao_estadual'),
            responsavel=payload.get('responsavel'),
            telefone=payload.get('telefone'),
            email=payload.get('email'),
            endereco=payload.get('endereco'),
            cidade=payload.get('cidade'),
            estado=payload.get('estado'),
            cep=payload.get('cep'),
            status=payload.get('status', 'ativo'),
            observacoes=payload.get('observacoes'),
            validade_contrato=payload.get('validade_contrato'),
            seguradora=payload.get('seguradora'),
            apolice=payload.get('apolice'),
            documento_anexo=payload.get('documento_anexo'),
            tipo_operacao=payload.get('tipo_operacao'),
        )
        self.db.add(tr)
        self.db.flush()
        return tr

    def get_by_cnpj(self, cnpj: str):
        return self.db.query(Transporter).filter(Transporter.cnpj == cnpj).first()

    def get(self, id: int):
        return self.db.query(Transporter).filter(Transporter.id == id).first()

    def list(self, filters: dict | None = None):
        q = self.db.query(Transporter)
        if filters:
            if 'razao_social' in filters:
                q = q.filter(Transporter.razao_social.ilike(f"%{filters['razao_social']}%"))
            if 'nome_fantasia' in filters:
                q = q.filter(Transporter.nome_fantasia.ilike(f"%{filters['nome_fantasia']}%"))
            if 'cnpj' in filters:
                q = q.filter(Transporter.cnpj == filters['cnpj'])
            if 'cidade' in filters:
                q = q.filter(Transporter.cidade.ilike(f"%{filters['cidade']}%"))
            if 'status' in filters:
                q = q.filter(Transporter.status == filters['status'])
        return q.order_by(Transporter.id.desc()).all()

    def update(self, id: int, payload: dict):
        tr = self.get(id)
        if not tr:
            return None
        for k, v in payload.items():
            if hasattr(tr, k) and k != 'id':
                setattr(tr, k, v)
        self.db.flush()
        return tr

    def delete(self, id: int):
        tr = self.get(id)
        if not tr:
            return False
        tr.status = 'inativo'
        self.db.flush()
        return True
