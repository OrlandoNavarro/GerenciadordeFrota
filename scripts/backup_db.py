import shutil
from pathlib import Path
from config.settings import settings


def _sqlite_path(url: str) -> Path:
    if url.startswith('sqlite:///'):
        return (Path.cwd() / url.replace('sqlite:///', '')).resolve()
    return Path.cwd() / 'fleet_management.db'


def backup(dest: str | None = None):
    src = _sqlite_path(settings.DATABASE_URL)
    if not src.exists():
        print('Database não encontrada:', src)
        return
    dest_path = Path(dest or (str(src) + '.backup'))
    shutil.copy(src, dest_path)
    print('Backup criado em', dest_path)


if __name__ == '__main__':
    backup()
