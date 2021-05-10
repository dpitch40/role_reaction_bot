import logging
import logging.config

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

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger('role_bot')
