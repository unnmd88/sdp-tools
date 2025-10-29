import logging.config

from core.config import BASE_DIR

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
        "file_users": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": BASE_DIR / 'users/logs/users.log',
            "formatter": "simple",
        },
    },
    "loggers": {
        "": {
            "level": "DEBUG",
            "handlers": ["console"],
            "propagate": True,
        },
        "users": {
            "level": "INFO",
            "handlers": ['console', 'file_users'],
            "propagate": True,
        },


    },
    "formatters": {
        # "verbose": {
        #     "format": "{name} {levelname} {asctime} {module} {lineno} {funcName} {message} ",
        #     "style": "{",
        # },
        "simple": {
            "format": "%(levelname)s %(message)s %(asctime)s %(filename)s %(lineno)s",
        },
    },
}

logging.config.dictConfig(LOGGING_CONFIG)


USERS_LOGGER = 'users'

# def logging_configure(level=logging.DEBUG):
#     console_handler = logging.StreamHandler()
#     file_handler = logging.FileHandler('logs/users.log')
#     logging.basicConfig(
#         level=level,
#         datefmt='%Y-%m-%d %H:%M:%S',
#         format='%(name)s - %(asctime)s - %(levelname)s - %(message)s  %(lineno)s',
#         handlers=[console_handler, file_handler],
#     )