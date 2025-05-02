import logging
import logging.config

# Custom Configuration class for app
from config import Config

def log_setup() -> None:
    # Bring in singleton instance class
    config = Config()

    # Set up variables
    env = config.ENV
    azure_conn = config.AZURE_CONN
    log_level = config.LOG_LEVEL
    log_file = config.LOG_FILE
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
                'level': log_level,
            },
            'file': {
                'class': 'logging.FileHandler',
                'formatter': 'default',
                'level': log_level,
                'filename': log_file,
            },
        },
        'root': {
            'handlers': root_handlers,
            'level': log_level,
        },
    }
    # Dynamic element to detect if an azure handler is needed
    if env == 'production' and azure_conn:
        logging_config['handlers']['azure'] = {
            'class': 'opencensus.ext.azure.log_exporter.AzureLogHandler',
            'level': log_level,
            'connection_string': azure_conn,
        }
        root_handlers.append('azure')

    # Set up global logging configuration - called once at the very beginning of application
    logging.config.dictConfig(logging_config)
    return None


# EOF

if __name__ == '__main__':
    print('This module is intended to be imported, not run directly.')