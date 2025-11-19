import logging
from logging.config import dictConfig

log_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "color": {
            "class": "colorlog.ColoredFormatter",
            "format": "%(log_color)s%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
            "log_colors": {
                "DEBUG": "cyan",
                "INFO": "green",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "bold_red",
            },
        },
        "default": {  # non-colored for file output
            "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "color",
            "stream": "ext://sys.stdout",
        },
    },

    "file": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "INFO",
            "formatter": "default",
            "filename": "app.log",
            "maxBytes": 1_000_000,  # rotate after ~1MB
            "backupCount": 3,       # keep 3 old logs
            "encoding": "utf8",
        },
    "loggers": {
        # this is your app's main logger
        "app": {"handlers": ["console"], "level": "DEBUG", "propagate": False},
    },
    # optional root config (so uvicorn etc. also log)
    "root": {"handlers": ["console"], "level": "INFO"},
}

# --- Apply config once ---
dictConfig(log_config)

# --- Make a get function ---
def get_logger(name: str = "app") -> logging.Logger:
    return logging.getLogger(name)