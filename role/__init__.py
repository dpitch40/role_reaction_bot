import logging
import logging.config
import os

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '%(asctime)s %(name)s %(pathname)s.%(lineno)d %(levelname)s: %(message)s'
        }
    },
    'handlers': {
        'stream': {
            'class': 'logging.StreamHandler',
            'level': logging.INFO,
            'formatter': 'default',
            'stream': 'ext://sys.stdout'
        }
    },
    'loggers': {
        'discord': {
            'level': logging.INFO,
            'propagate': False,
            'handlers': ['stream']
        }
    },
    'root': {
        'level': logging.INFO,
        'handlers': ['stream']
    }
}

if 'LOGFILE' in os.environ:
    LOGGING_CONFIG['handlers']['file'] = {
        'class': 'logging.handlers.RotatingFileHandler',
        'level': logging.INFO,
        'formatter': 'default',
        'filename': os.environ['LOGFILE'],
        'maxBytes': 2 ** 20,
        'backupCount': 10,
    }
    LOGGING_CONFIG['root']['handlers'].append('file')
    LOGGING_CONFIG['loggers']['discord']['handlers'].append('file')

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger('role_bot')
