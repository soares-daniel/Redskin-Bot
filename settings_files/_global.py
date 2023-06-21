import os

SETTINGS_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SETTINGS_DIR)
DATA_DIR = os.path.join(ROOT_DIR, 'data')

# Discord
DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
DISCORD_CLIENT_SECRET = os.getenv('DISCORD_CLIENT_SECRET')
DISCORD_CLIENT_ID = os.getenv('DISCORD_CLIENT_ID')

# PRD API
USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')
API_UR = os.getenv('API_URL')
EVENT_ENDPOINT = os.getenv('EVENT_ENDPOINT')
