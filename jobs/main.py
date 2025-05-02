# jobs/main.py
# File to be executed fo ETL processing. Parent, top-level executor
# Log initializer should be started here for trickle downs
from ext_lib import log_setup
import logging
log_setup()
log = logging.getLogger(__name__)

# Import dependencies
from argparse import ArgumentParser, Namespace
from dotenv import load_dotenv

# Custom libraries
from .pipeline import Pipeline_Runner, ETL_Config


# Command Line Interface namespace class for linter type checking
class CLIArgs(Namespace):
    pipeline: str
    config: str

def main() -> None:
    # Bring in environment variables first
    load_dotenv()
    

    # Create argument parsers
    parser = ArgumentParser(
        description = 'Run one of the configured ETL pipelines.'
    )
    parser.add_argument(
        'pipeline'
        ,help = 'The name of the pipeline to run.'
    )
    parser.add_argument(
        '--config'
        ,default = 'config/pipeline.yml'
        ,help = 'Path to the YAML Pipeline (default: %(default)s)'
        ,dest = 'config'
    )

    # Grab arguments
    args = parser.parse_args(namespace = CLIArgs())

    # Create the configuration
    cfg = ETL_Config.from_yaml(args.config)

    # Instantiate the runner
    runner = Pipeline_Runner(cfg)

    # Kick off pipeline
    runner.run(args.pipeline)

    return None


if __name__ == '__main__':
    main()

# EOF