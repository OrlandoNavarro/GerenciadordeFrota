from domain.repositories.vehicle_repository import VehicleRepository


class VehicleService:
    def __init__(self, db_session):
        self.db = db_session
        self.repo = VehicleRepository(db_session)

    def create_vehicle(self, payload: dict):
        if not payload.get('placa'):
            raise ValueError('Placa é obrigatória')
        return self.repo.create(payload)

    def list_vehicles(self, filters: dict | None = None):
        return self.repo.list(filters)

    def get_vehicle(self, id: int):
        return self.repo.get(id)

    def update_vehicle(self, id: int, payload: dict):
        return self.repo.update(id, payload)

    def delete_vehicle(self, id: int):
        return self.repo.delete(id)
