from config.database import SessionLocal
from domain.repositories.user_repository import UserRepository


def create_admin(email='admin@local', password='admin123'):
    db = SessionLocal()
    repo = UserRepository(db)
    if not repo.get_by_email(email):
        repo.create_user({'email': email, 'password': password, 'full_name': 'Admin', 'role': 'admin'})
        db.commit()
        print('Admin created')
    else:
        print('Admin already exists')


if __name__ == '__main__':
    create_admin()
