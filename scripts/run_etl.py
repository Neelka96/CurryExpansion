# jobs/main.py
# File to be executed fo ETL processing. Parent, top-level executor

# Import dependencies
from argparse import ArgumentParser, Namespace
from dotenv import load_dotenv
import logging

# Custom libraries
from logger import log_setup
from factory import get_settings
from ETL import Pipeline_Runner


# CLI class for namespace linking and linter assistance
class CLIArgs(Namespace):
    name: str
    config: str

def main() -> None:
    load_dotenv()   # Bring in environment variables first
    get_settings()  # Initialize settings for the 1st time - saved in lru_cache
    log_setup()     # Master log setup with Settings obj for lower-level files
    log = logging.getLogger(__name__)

    # Create argument parsers
    parser = ArgumentParser(description = 'Run one of the configured ETL pipelines.')
    parser.add_argument(
        'name',
        help = 'The name of the task (pipeline grouping) or single pipeline to run.'
    )
    parser.add_argument(
        '--config',
        default = 'config/pipeline.yml',
        help = 'Path to the YAML Pipeline (default: %(default)s)',
        dest = 'config'
    )

    # Grab arguments
    args = parser.parse_args(namespace = CLIArgs())
    
    # Instantiate the runner
    runner = Pipeline_Runner(etl_cfg_path = args.config)

    # Kick off pipeline
    runner.run(args.name)

    return None


if __name__ == '__main__':
    main()

# EOF