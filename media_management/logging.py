import colorlog
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'colored': {
            '()': colorlog.ColoredFormatter,
            'format': '%(log_color)s%(levelname)s%(reset)s [%(asctime)s]: \n\t  %(green)s%(module)s: %(reset)s %(purple)s%(message)s \n\n',
            'datefmt': '%Y-%m-%d %H:%M:%S',
            'log_colors': {
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'red,bg_white',
            },
            'secondary_log_colors': {
                'message': {
                    'ERROR': 'light_red',
                    'CRITICAL': 'light_red'
                },
            },
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'colored',
            'filters': [],
        },
        'view_console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'colored',
            'filters': [],
        },
        # 'user_logs': {
        #     'level': 'INFO',
        #     'class': 'logging.handlers.RotatingFileHandler',
        #     'filename': f'{BASE_DIR}/logs/user.log',
        #     'formatter': 'colored',
        #     'maxBytes': 1024*1024*30,  # 30 MB
        #     'filters': [],
        #     'backupCount': 5,  # Backup up to 5 log files
        #     'encoding': 'utf-8',
        # },
    },
    'loggers': {
        '': {
            'handlers': ['console',],
            'level': 'INFO',
        },

        'view': {
            'handlers': ['view_console'],
            'level': 'INFO',
            'propagate': False
        }
    },
}
