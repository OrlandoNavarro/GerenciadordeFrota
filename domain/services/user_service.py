from domain.repositories.user_repository import UserRepository


class UserService:
    def __init__(self, db_session):
        self.db = db_session
        self.repo = UserRepository(db_session)

    def create_user(self, data: dict):
        # Validate basic fields
        if not data.get('email') or not data.get('password'):
            raise ValueError('Email e senha são obrigatórios')
        return self.repo.create_user(data)

    def authenticate(self, email: str, password: str):
        user = self.repo.get_by_email(email)
        if not user:
            return None
        from passlib.hash import bcrypt
        if not bcrypt.verify(password, user.password_hash):
            return None
        return user
