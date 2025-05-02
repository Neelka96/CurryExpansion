# jobs/main.py
# File to be executed fo ETL processing. Parent, top-level executor
# Log initializer should be started here for trickle downs
from ext_lib import log_setup
import logging
log_setup()
log = logging.getLogger(__name__)

from .pipeline import Pipeline_Runner
from argparse import ArgumentParser, Namespace

class CLIArgs(Namespace):
    pipeline: str
    config: str


def main() -> None:
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

    # Instantiate the runner
    runner = Pipeline_Runner(args.config)

    # Kick off pipeline
    runner.run(args.pipeline)

    return None


if __name__ == '__main__':
    main()

# EOF