from domain.services.vehicle_service import VehicleService


def test_create_vehicle(db_session):
    svc = VehicleService(db_session)
    v = svc.create_vehicle({'placa':'TST1234','modelo':'X','marca':'Y'})
    db_session.commit()
    assert v.id is not None
