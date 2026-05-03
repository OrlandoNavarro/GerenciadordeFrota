from domain.repositories.document_repository import DocumentRepository


class DocumentService:
    def __init__(self, db_session):
        self.db = db_session
        self.repo = DocumentRepository(db_session)

    def create_document(self, payload: dict):
        return self.repo.create(payload)

    def list_documents(self, filters: dict | None = None):
        return self.repo.list(filters)

    def get_document(self, id: int):
        return self.repo.get(id)

    def update_document(self, id: int, payload: dict):
        return self.repo.update(id, payload)

    def delete_document(self, id: int):
        return self.repo.delete(id)
