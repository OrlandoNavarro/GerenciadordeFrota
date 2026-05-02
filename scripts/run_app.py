import os
import subprocess
import sys


def main():
    cmd = [sys.executable, '-m', 'streamlit', 'run', os.path.join(os.path.dirname(__file__), '..', 'app.py')]
    subprocess.run(cmd)


if __name__ == '__main__':
    main()
