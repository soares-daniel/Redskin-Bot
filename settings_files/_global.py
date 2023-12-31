import os

SETTINGS_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SETTINGS_DIR)
DATA_DIR = os.path.join(ROOT_DIR, 'data')

SERVER_PORT = os.getenv('SERVER_PORT')
SERVER_HOST = os.getenv('SERVER_HOST')
NOTIFICATION_ENDPOINT = os.getenv('NOTIFICATION_ENDPOINT')
GUILD_ID = os.getenv('GUILD_ID')

# Discord
DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
DISCORD_CLIENT_SECRET = os.getenv('DISCORD_CLIENT_SECRET')
DISCORD_CLIENT_ID = os.getenv('DISCORD_CLIENT_ID')

# PRD API
USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')
API_HOST = os.getenv('API_HOST')
API_SERVER_PORT = os.getenv('API_SERVER_PORT')
API_ENDPOINT = os.getenv('API_ENDPOINT')
EVENT_ENDPOINT = os.getenv('EVENT_ENDPOINT')
API_URL = f'http://{API_HOST}:{API_SERVER_PORT}{API_ENDPOINT}'

# Calendar
CATEGORY_NAME = os.getenv('CATEGORY_NAME')
NOTIFICATION_CHANNEL_NAME = os.getenv('NOTIFICATION_CHANNEL_NAME')
CALENDAR_CHANNEL_NAME = os.getenv('CALENDAR_CHANNEL_NAME')
COMMAND_CHANNEL_NAME = os.getenv('COMMAND_CHANNEL_NAME')
EVENT_CHANNEL_NAME = os.getenv('EVENT_CHANNEL_NAME')

# Database Embed Images
USER_IMAGE_URL = os.getenv('USER_IMAGE_URL')
ROLE_IMAGE_URL = os.getenv('ROLE_IMAGE_URL')
EVENT_IMAGE_URL = os.getenv('EVENT_IMAGE_URL')
EVENT_TYPE_IMAGE_URL = os.getenv('EVENT_TYPE_IMAGE_URL')
PERMISSION_IMAGE_URL = os.getenv('PERMISSION_IMAGE_URL')
