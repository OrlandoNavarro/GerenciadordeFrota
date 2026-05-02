from domain.services.transporter_service import TransporterService


def test_create_transporter(db_session):
    svc = TransporterService(db_session)
    tr = svc.create_transporter({'razao_social':'A','cnpj':'1112223330001'})
    db_session.commit()
    assert tr.id is not None
