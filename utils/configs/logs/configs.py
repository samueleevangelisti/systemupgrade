'''
configs.py
'''
from utils import paths



IS_DEBUG = False
IS_FILE = False
LOG_PATH = paths.resolve_path(paths.get_folder_path(__file__), '../../../logs/log.log')
RETENTION_DAYS = 365
