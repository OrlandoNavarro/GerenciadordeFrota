from domain.repositories.trip_repository import TripRepository


class TripService:
    def __init__(self, db_session):
        self.db = db_session
        self.repo = TripRepository(db_session)

    def create_trip(self, payload: dict):
        return self.repo.create(payload)

    def list_trips(self, filters: dict | None = None):
        return self.repo.list(filters)
