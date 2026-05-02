from passlib.hash import bcrypt
from domain.repositories.user_repository import UserRepository


def hash_password(password: str) -> str:
    return bcrypt.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    try:
        return bcrypt.verify(password, hashed)
    except Exception:
        return False


def authenticate(email: str, password: str, db_session) -> dict | None:
    repo = UserRepository(db_session)
    user = repo.get_by_email(email)
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user
