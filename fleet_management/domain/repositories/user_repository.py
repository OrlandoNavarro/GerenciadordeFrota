from domain.models.user import User
from passlib.hash import bcrypt


class UserRepository:
    def __init__(self, db_session):
        self.db = db_session

    def create_user(self, data: dict) -> User:
        # Expect keys: email, full_name, password, role
        existing = self.get_by_email(data.get('email'))
        if existing:
            raise ValueError('Email already exists')
        hashed = bcrypt.hash(data.get('password'))
        user = User(
            email=data.get('email'),
            full_name=data.get('full_name'),
            password_hash=hashed,
            role=data.get('role', 'operador'),
        )
        self.db.add(user)
        self.db.flush()
        return user

    def get_by_email(self, email: str):
        return self.db.query(User).filter(User.email == email).first()

    def get_by_id(self, id: int):
        return self.db.query(User).filter(User.id == id).first()

    def list(self, skip: int = 0, limit: int = 100):
        return self.db.query(User).offset(skip).limit(limit).all()
