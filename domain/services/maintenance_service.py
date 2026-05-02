from domain.repositories.maintenance_repository import MaintenanceRepository


class MaintenanceService:
    def __init__(self, db_session):
        self.db = db_session
        self.repo = MaintenanceRepository(db_session)

    def create_maintenance(self, payload: dict):
        return self.repo.create(payload)

    def list_maintenances(self, filters: dict | None = None):
        return self.repo.list(filters)

    def get_maintenance(self, id: int):
        return self.repo.get(id)

    def update_maintenance(self, id: int, payload: dict):
        return self.repo.update(id, payload)

    def delete_maintenance(self, id: int):
        return self.repo.delete(id)
