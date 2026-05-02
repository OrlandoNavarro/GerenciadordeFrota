from domain.repositories.document_repository import DocumentRepository


class DocumentService:
    def __init__(self, db_session):
        self.db = db_session
        self.repo = DocumentRepository(db_session)

    def create_document(self, payload: dict):
        return self.repo.create(payload)
