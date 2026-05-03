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
        # Support multiple password storage strategies for development:
        # - bcrypt hashes (standard, verified via core.auth.verify_password)
        # - plain:... prefix (development fallback)
        pw = getattr(user, 'password_hash', '') or ''
        if pw.startswith('plain:'):
            expected = pw.split(':', 1)[1]
            if password == expected:
                return user
            return None

        # Fallback to bcrypt verification (wrapped to handle missing libs)
        from core.auth import verify_password
        if not verify_password(password, pw):
            return None
        return user

    def get_user(self, id: int):
        return self.repo.get_by_id(id)

    def list_users(self, skip: int = 0, limit: int = 100):
        return self.repo.list(skip=skip, limit=limit)

    def update_user(self, id: int, payload: dict):
        return self.repo.update_user(id, payload)
