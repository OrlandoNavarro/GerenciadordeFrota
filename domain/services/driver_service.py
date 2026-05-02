from domain.repositories.driver_repository import DriverRepository
from core.utils import sanitize_cpf


class DriverService:
    def __init__(self, db_session):
        self.db = db_session
        self.repo = DriverRepository(db_session)

    def create_driver(self, payload: dict):
        if not payload.get('nome') or not payload.get('cpf'):
            raise ValueError('Nome e CPF são obrigatórios')
        payload['cpf'] = sanitize_cpf(payload.get('cpf'))
        if self.repo.get_by_cpf(payload['cpf']):
            raise ValueError('CPF já cadastrado')
        return self.repo.create(payload)

    def get_driver(self, id: int):
        return self.repo.get(id)

    def list_drivers(self, filters: dict | None = None):
        return self.repo.list(filters)

    def update_driver(self, id: int, payload: dict):
        if 'cpf' in payload:
            payload['cpf'] = sanitize_cpf(payload.get('cpf'))
        return self.repo.update(id, payload)

    def delete_driver(self, id: int):
        return self.repo.delete(id)
