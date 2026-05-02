import pytest
from domain.services.driver_service import DriverService


def test_create_driver(db_session):
    svc = DriverService(db_session)
    d = svc.create_driver({'nome': 'Joao', 'cpf': '12345678901'})
    db_session.commit()
    assert d.id is not None


def test_duplicate_cpf_raises(db_session):
    svc = DriverService(db_session)
    svc.create_driver({'nome': 'Ana', 'cpf': '11122233344'})
    db_session.commit()
    with pytest.raises(ValueError):
        svc.create_driver({'nome': 'Pedro', 'cpf': '11122233344'})
