from pathlib import Path

APP_DIR = Path(__file__).resolve().parent.parent
SRC_DIR = APP_DIR.parent
ROOT_DIR = SRC_DIR.parent

# App settings
TEMPLATES_DIR = APP_DIR / 'templates'
STATIC_DIR = APP_DIR / 'static'
DATA_DIR = APP_DIR / 'data'
EVENTS_DIR = DATA_DIR / 'events'
IMAGES_DIR = STATIC_DIR / 'images'

# Build settings
SITE_DIR = ROOT_DIR / 'site'
SITE_STATIC_DIR = SITE_DIR / 'static'
