from pathlib import Path

CSS_PATH = Path(__file__).parent.parent / 'assets' / 'styles' / 'md3.css'

def load_theme_css():
    try:
        return CSS_PATH.read_text()
    except Exception:
        return ''
