from domain.services.user_service import UserService


def test_create_and_authenticate(db_session):
    svc = UserService(db_session)
    user = svc.create_user({'email': 't@t.com', 'password': 'pass123', 'full_name': 'T', 'role': 'admin'})
    db_session.commit()
    auth = svc.authenticate('t@t.com', 'pass123')
    assert auth is not None
    assert auth.email == 't@t.com'
