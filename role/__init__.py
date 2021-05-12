import logging
import logging.config
import os

class GuildNameFilter(logging.Filter):
    def filter(self, record):
        if hasattr(record, 'guild'):
            record.guildname = f' ({record.guild.name})'
        else:
            record.guildname = ''
        return True

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '%(asctime)s %(name)s %(filename)s.%(lineno)d %(levelname)s: %(message)s'
        },
        'discord': {
            'format': '%(asctime)s %(name)s %(filename)s.%(lineno)d %(levelname)s%(guildname)s: %(message)s'
        }
    },
    'filters': {
        'add_guild_name': {
            '()': GuildNameFilter
        },
    },
    'handlers': {
        'stream': {
            'class': 'logging.StreamHandler',
            'level': logging.INFO,
            'formatter': 'default',
            'stream': 'ext://sys.stdout'
        },
        'discord_stream': {
            'class': 'logging.StreamHandler',
            'level': logging.INFO,
            'formatter': 'discord',
            'stream': 'ext://sys.stdout'
        }
    },
    'loggers': {
        'role_bot': {
            'level': logging.INFO,
            'propagate': False,
            'handlers': ['discord_stream'],
            'filters': ['add_guild_name']
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
    LOGGING_CONFIG['handlers']['file_discord'] = LOGGING_CONFIG['handlers']['file'].copy()
    LOGGING_CONFIG['handlers']['file_discord']['formatter'] = 'discord'
    LOGGING_CONFIG['root']['handlers'].append('file')
    LOGGING_CONFIG['loggers']['role_bot']['handlers'].append('file_discord')

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger('role_bot')
