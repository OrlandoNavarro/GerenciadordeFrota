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

    def list(self, filters: dict | None = None):
        q = self.db.query(Document)
        return q.all()
