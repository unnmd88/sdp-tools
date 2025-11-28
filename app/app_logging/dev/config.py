import logging.config

from core.config import API_V1_PATH, BASE_DIR

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'file_users': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'auth/logs/users.log',
            'formatter': 'simple',
        },
        'file_passports': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': API_V1_PATH / 'passports/logs/log.log',
            'formatter': 'simple2',
        },
        'file_passport_groups': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': API_V1_PATH / 'passport_groups/logs/log.log',
            'formatter': 'simple2',
        },
    },
    'loggers': {
        '': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': True,
        },
        'users': {
            'level': 'INFO',
            'handlers': ['console', 'file_users'],
            'propagate': True,
        },
        'passports': {
            'level': 'INFO',
            'handlers': ['console', 'file_passports'],
        },
        'passport_groups': {
            'level': 'INFO',
            'handlers': ['console', 'file_passport_groups'],
        },
    },
    'formatters': {
        # "verbose": {
        #     "format": "{name} {levelname} {asctime} {module} {lineno} {funcName} {message} ",
        #     "style": "{",
        # },
        'simple': {
            'format': '%(levelname)s %(message)s %(asctime)s %(filename)s %(lineno)s',
        },
        'simple2': {
            'format': '%(asctime)s %(levelname)s %(message)s %(filename)s %(lineno)s',
        },
    },
}

logging.config.dictConfig(LOGGING_CONFIG)


USERS_LOGGER = 'users'
PASSPORTS_LOGGER = 'passports'
PASSPORTS_OWNERS_LOGGER = 'passport_groups'

# def logging_configure(level=logging.DEBUG):
#     console_handler = logging.StreamHandler()
#     file_handler = logging.FileHandler('logs/users.log')
#     logging.basicConfig(
#         level=level,
#         datefmt='%Y-%m-%d %H:%M:%S',
#         format='%(name)s - %(asctime)s - %(levelname)s - %(message)s  %(lineno)s',
#         handlers=[console_handler, file_handler],
#     )

"""
Config example:
# Source - https://stackoverflow.com/a
# Posted by Chris, modified by community. See post 'Timeline' for change history
# Retrieved 2025-11-11, License - CC BY-SA 4.0

LOGGING_CONFIG = { 
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': { 
        'standard': { 
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
        'custom_formatter': { 
            'format': "%(asctime)s [%(processName)s: %(process)d] [%(threadName)s: %(thread)d] [%(levelname)s] %(name)s: %(message)s"
            
        },
    },
    'handlers': { 
        'default': { 
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',  # Default is stderr
        },
        'stream_handler': { 
            'formatter': 'custom_formatter',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',  # Default is stderr
        },
        'file_handler': { 
            'formatter': 'custom_formatter',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'app.log',
            'maxBytes': 1024 * 1024 * 1, # = 1MB
            'backupCount': 3,
        },
    },
    'loggers': { 
        'uvicorn': {
            'handlers': ['default', 'file_handler'],
            'level': 'TRACE',
            'propagate': False
        },
        'uvicorn.access': {
            'handlers': ['stream_handler', 'file_handler'],
            'level': 'TRACE',
            'propagate': False
        },
        'uvicorn.error': { 
            'handlers': ['stream_handler', 'file_handler'],
            'level': 'TRACE',
            'propagate': False
        },
        'uvicorn.asgi': {
            'handlers': ['stream_handler', 'file_handler'],
            'level': 'TRACE',
            'propagate': False
        },

    },
}

"""
