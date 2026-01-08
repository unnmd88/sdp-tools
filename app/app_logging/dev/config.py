import logging.config

from core.config import API_V1_PATH, BASE_DIR

print(f'BASE_DIR: {BASE_DIR}')

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'RUD': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'app_logging/RUD.log',
            'formatter': 'simple2',
        },
        'USERS_RUD': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'app_logging/USERS_RUD.log',
            'formatter': 'simple2',
        },
        'auth': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'app_logging/auth.log',
            'formatter': 'simple2',
        },
        'JWT': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'app_logging/jwt.log',
            'formatter': 'simple2',
        },
    },
    'loggers': {
        '': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': True,
        },
        'common': {
            'level': 'INFO',
            'handlers': ['RUD'],
            'propagate': True,
        },
        'auth': {
            'level': 'INFO',
            'handlers': ['auth'],
            'propagate': True,
        },
        'jwt': {
            'level': 'INFO',
            'handlers': ['JWT'],
            'propagate': True,
        },
        'users': {
            'level': 'INFO',
            'handlers': ['USERS_RUD'],
            'propagate': True,
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

COMMON_LOGGER = 'common'
USERS_LOGGER = 'users'
JWT_LOGGER = 'jwt'
AUTH_LOGGER = 'auth'


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
