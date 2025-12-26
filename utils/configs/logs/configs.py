'''
configs.py
'''
from utils import paths



IS_DEBUG = True
IS_FILE = False
FOLDER_PATH = paths.resolve_path(paths.get_folder_path(__file__), '../../../logs/')
LOG_PATH = paths.resolve_path(FOLDER_PATH, 'log.log')
