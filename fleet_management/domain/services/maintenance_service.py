from domain.repositories.maintenance_repository import MaintenanceRepository


class MaintenanceService:
    def __init__(self, db_session):
        self.db = db_session
        self.repo = MaintenanceRepository(db_session)

    def create_maintenance(self, payload: dict):
        return self.repo.create(payload)
