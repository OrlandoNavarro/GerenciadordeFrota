from domain.repositories.driver_repository import DriverRepository


class DriverService:
    def __init__(self, db_session):
        self.db = db_session
        self.repo = DriverRepository(db_session)

    def create_driver(self, payload: dict):
        if not payload.get('nome') or not payload.get('cpf'):
            raise ValueError('Nome e CPF são obrigatórios')
        return self.repo.create(payload)

    def list_drivers(self, filters: dict | None = None):
        return self.repo.list(filters)
