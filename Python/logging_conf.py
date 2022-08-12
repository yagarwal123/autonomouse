from config import CONFIG
LOGGING_CONFIG = {
    'version': 1,
    'loggers': {
        '': {  # root logger
            'level': 'NOTSET',
            'handlers': ['debug_console_handler', 'info_rotating_file_handler', 'warning_file_handler','error_mail_handler'],
        },
        'my.package': { 
            'level': 'WARNING',
            'propagate': False,
            'handlers': ['info_rotating_file_handler', 'warning_file_handler','error_mail_handler' ],
        },
    },
    'handlers': {
        'debug_console_handler': {
            'level': 'DEBUG',
            'formatter': 'info',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
        },
        'info_rotating_file_handler': {
            'level': 'INFO',
            'formatter': 'info',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': f'{CONFIG.application_path}/info.log',
            'mode': 'a',
            'maxBytes': 1048576,
            'backupCount': 10
        },
        'warning_file_handler': {
            'level': 'WARNING',
            'formatter': 'warning',
            'class': 'logging.FileHandler',
            'filename': f'{CONFIG.application_path}/warning.log',
            'mode': 'a',
        },
        'error_mail_handler': {
            'level': 'ERROR',
            'formatter': 'warning',
            'class': 'logging.handlers.SMTPHandler',
            'mailhost' : ('smtp.gmail.com', 587),
            'fromaddr': CONFIG.EMAIL_ID,
            'toaddrs': CONFIG.TO_EMAIL,
            'subject': 'Error with autonomouse',
            'credentials':(CONFIG.EMAIL_ID,CONFIG.PASSWORD),
            'secure':()
        }
    },
    'formatters': {
        'info': {
            'format': '%(asctime)s-%(levelname)s-%(name)s::%(module)s|%(lineno)s:: %(message)s'
        },
        'warning': {
            'format': '%(asctime)s-%(levelname)s-%(name)s-%(process)d::%(module)s|%(lineno)s:: %(message)s'
        },
    },

}