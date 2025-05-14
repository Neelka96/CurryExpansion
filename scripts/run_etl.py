# main.py
# File to be executed fo ETL processing. Parent, top-level executor

# Import dependencies
from argparse import ArgumentParser, Namespace
from dotenv import load_dotenv
from pathlib import Path
import logging

# Custom libraries
from core import log_setup, get_settings, log_exceptions
from ETL import TaskRunner


# CLI class for namespace linking and linter assistance
class CLIArgs(Namespace):
    name: str
    config: str

@log_exceptions
def main() -> None:
    load_dotenv()               # Bring in environment variables first
    env_cfg = get_settings()    # Initialize settings for the 1st time - saved in lru_cache
    log_setup(env_cfg)          # Master log setup with Settings obj for lower-level files
    log = logging.getLogger(__name__)

    # Extra debug log for settings
    log.info('ETL Top-Level accessed. Configured for environment: %s.' % env_cfg.app_env)
    log.debug('Key variables parsed include {Storage Path: %s, Database Name: %s}', env_cfg.storage, env_cfg.db_name)

    # Create argument parsers
    parser = ArgumentParser(description = 'Run one of the configured ETL pipelines.')
    parser.add_argument(
        'name',
        help = 'The name of the task (pipeline grouping) or single pipeline to run.'
    )
    parser.add_argument(
        '--config',
        default = 'ETL/pipeline.yml',
        help = 'Path to the YAML Pipeline (default: %(default)s)',
        dest = 'config'
    )

    # Grab arguments
    args = parser.parse_args(namespace = CLIArgs())

    # Arguments are:
    etl_cfg_path = Path(args.config).resolve()
    task_or_pipe_name = args.name
    
    # Logs for CLI arguments
    log.debug('Initializing TaskRunner with ETL config file: %s.' % etl_cfg_path)

    # Instantiate the runner
    runner = TaskRunner(etl_cfg_path = str(etl_cfg_path))

    # Another log for the kickoff
    log.debug('Kicking off pipeline, locating name/task: %s.' % task_or_pipe_name)

    # Kick off pipeline
    runner.run(task_or_pipe_name)

    return None


if __name__ == '__main__':
    main()

# EOF