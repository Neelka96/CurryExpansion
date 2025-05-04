# Import dependencies
import logging.config
import logging

# Custom libraries
from factory import get_settings


def log_setup() -> None:
    # Get the settings (first time or from the factory cache)
    cfg = get_settings()

    # Add more handlers here if necessary
    root_handlers: list[str] = ['console', 'file']

    # Explicit logging dictionary
    logging_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'default': {
                'format': '%(asctime)s %(name)s: %(levelname)s - %(message)s',
                'datefmt': '%m-%d-%y %H:%M:%S'
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'default',
                'level': cfg.log_level,
            },
            'file': {
                'class': 'logging.FileHandler',
                'formatter': 'default',
                'level': cfg.log_level,
                'filename': cfg.log_file,
            },
        },
        'root': {
            'handlers': root_handlers,
            'level': cfg.log_level,
        },
    }
    # Detect if azure logger is needed, and if so build and add it to the root handlers
    if cfg.app_env == 'production':
        logging_config['handlers']['azure'] = {
            'class': 'opencensus.ext.azure.log_exporter.AzureLogHandler',
            'level': cfg.log_level,
            'connection_string': cfg.caas_conn,
        }
        root_handlers.append('azure')

    # Set up global logging configuration - called once at the very beginning of application
    logging.config.dictConfig(logging_config)
    return None


# EOF

if __name__ == '__main__':
    print('This module is intended to be imported, not run directly.')