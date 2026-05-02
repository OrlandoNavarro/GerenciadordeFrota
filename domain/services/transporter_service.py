from domain.repositories.transporter_repository import TransporterRepository
from core.utils import sanitize_cnpj


class TransporterService:
    def __init__(self, db_session):
        self.db = db_session
        self.repo = TransporterRepository(db_session)

    def create_transporter(self, payload: dict):
        if not payload.get('razao_social') or not payload.get('cnpj'):
            raise ValueError('Razão social e CNPJ são obrigatórios')
        payload['cnpj'] = sanitize_cnpj(payload.get('cnpj'))
        return self.repo.create(payload)

    def list_transporters(self, filters: dict | None = None):
        return self.repo.list(filters)

    def get_transporter(self, id: int):
        return self.repo.get(id)

    def update_transporter(self, id: int, payload: dict):
        # Sanitize cnpj if present
        if 'cnpj' in payload:
            payload['cnpj'] = sanitize_cnpj(payload.get('cnpj'))
        return self.repo.update(id, payload)

    def delete_transporter(self, id: int):
        return self.repo.delete(id)
