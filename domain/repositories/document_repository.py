from domain.models.document import Document


class DocumentRepository:
    def __init__(self, db_session):
        self.db = db_session

    def create(self, payload: dict) -> Document:
        d = Document(
            tipo_documento=payload.get('tipo_documento'),
            categoria_referencia=payload.get('categoria_referencia'),
            referencia_id=payload.get('referencia_id'),
            numero=payload.get('numero'),
            data_emissao=payload.get('data_emissao'),
            data_vencimento=payload.get('data_vencimento'),
            status=payload.get('status', 'vigente'),
            observacoes=payload.get('observacoes'),
        )
        self.db.add(d)
        self.db.flush()
        return d

    def get(self, id: int):
        return self.db.query(Document).filter(Document.id == id).first()

    def list(self, filters: dict | None = None):
        q = self.db.query(Document)
        if filters:
            if 'tipo_documento' in filters and filters.get('tipo_documento'):
                q = q.filter(Document.tipo_documento.ilike(f"%{filters['tipo_documento']}%"))
            if 'numero' in filters and filters.get('numero'):
                q = q.filter(Document.numero.ilike(f"%{filters['numero']}%"))
            if 'status' in filters and filters.get('status'):
                q = q.filter(Document.status == filters['status'])
            if 'categoria_referencia' in filters and filters.get('categoria_referencia'):
                q = q.filter(Document.categoria_referencia == filters['categoria_referencia'])
            if 'referencia_id' in filters and filters.get('referencia_id') is not None:
                q = q.filter(Document.referencia_id == filters['referencia_id'])
            if 'date_from' in filters and filters.get('date_from'):
                q = q.filter(Document.data_emissao >= filters['date_from'])
            if 'date_to' in filters and filters.get('date_to'):
                q = q.filter(Document.data_emissao <= filters['date_to'])
        return q.order_by(Document.id.desc()).all()

    def update(self, id: int, payload: dict):
        d = self.get(id)
        if not d:
            return None
        for k, v in payload.items():
            if hasattr(d, k) and k != 'id':
                setattr(d, k, v)
        self.db.flush()
        return d

    def delete(self, id: int):
        d = self.get(id)
        if not d:
            return False
        d.status = 'cancelado'
        self.db.flush()
        return True
