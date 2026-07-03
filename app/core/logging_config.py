LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": "%(asctime)s %(levelprefix)s [%(module)10s:%(lineno)-3d] - %(message)s",
            "use_colors": True,
        },
        "access": {
            "()": "uvicorn.logging.AccessFormatter",
            "fmt": '%(asctime)s %(levelprefix)s [%(client_addr)s] - %(request_line)s" %(status_code)s',
            "use_colors": True,
        },
    },
    "handlers": {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
        "access": {
            "formatter": "access",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
    },
    "loggers": {
        "uvicorn.error": {"level": "INFO"},
        "uvicorn.access": {"handlers": ["access"], "level": "INFO", "propagate": True},
        # "sqlalchemy.engine": {
        #     "handlers": ["default"],
        #     "level": "INFO",
        #     "propagate": False,
        # },
    },
    "root": {
        "handlers": ["default"],
        "level": "DEBUG",
        "propagate": False,
    },
}
