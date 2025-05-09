# Import dependencies
from typing import overload, Literal
from importlib import import_module

# Allow logging from top-level
import logging
log = logging.getLogger(__name__)

# Custom libraries
from core import log_exceptions
from ETL.etl_bin import BaseExtractor, BaseTransformer, BaseLoader, Component_Block, Pipeline_Block, Task_Block, ETL_Config


class Pipeline_Runner:
    '''
    The Pipeline Runner is an abstraction of the ETL process meant to be orchestrated from the pipeline.yml file.  
    The top-level parent file that creates an instantiation must load in environment variables first via `dotenv.load_dotenv()` to ensure they're expanded properly.
    After instantiation, execute method `.run(YOUR_PIPELINE_NAME_HERE)` to run a specific pipeline in the yaml.

    :param config_path: String path where pipeline.yml lives.
    :type config_path: str
    
    :returns: Abstracted Pipeline containing the parsed yaml. Ready for specific pipeline execution.
    :rtype: Pipeline_Runner
    '''
    def __init__(self, etl_cfg_path: str):
        self.etl_cfg = ETL_Config.from_yaml(etl_cfg_path)
    
    # Type checks implementation for each component type and its corresponding base ETL part
    @overload
    def _make(self, component_type: Literal['extractors'],     name: str) -> BaseExtractor: ...
    @overload
    def _make(self, component_type: Literal['transformers'],   name: str) -> BaseTransformer: ...
    @overload
    def _make(self, component_type: Literal['loaders'],        name: str) -> BaseLoader: ...

    # Actual function definition with all variations
    def _make(self, component_type: Literal['extractors', 'transformers', 'loaders'], name: str) -> BaseExtractor | BaseTransformer | BaseLoader:
        '''Constructs an instance of a designated class with loaded parameters from the pipeline.yml.

        :param component_type: Specific section of pipeline building blocks.
        :type component_type: Literal[&#39;extractors&#39;, &#39;transformers&#39;, &#39;loaders&#39;]
        :param name: The title of the exact block to grab.
        :type name: str

        :returns: Always returns one of three base ETL object classes, linked to real classes in the ETL/ files.
        :rtype: BaseExtractor or BaseTransformer or BaseLoader
        '''
        # Gets the actual class specified by the YAML for pipeline and construct with paramaters
        comp_cfg: Component_Block = getattr(self.etl_cfg, component_type)[name]
        module_name, cls_name = comp_cfg.class_name.rsplit('.', 1)
        Impl = getattr(import_module(module_name), cls_name)
        log.debug('Crafting import %s.%s.', (module_name, cls_name))
        return Impl(**(comp_cfg.params or {}))

    # Execution for pipeline begins and ends here
    def _run_single_pipeline(self, pipeline: str) -> None:
        '''
        Actual running of any pipeline (requires the linking of abstract ETL classes from ext_lib). 
        Not meant for external use `.run(task_or_pipe)` instead as it accepts a task or pipeline name.

        :param pipeline: Name of pipeline to run
        :type pipeline: str

        :returns: No return on success. See logging file for details.
        :rtype: None
        '''
        # Log pipeline start
        log.info('Pipeline %s started.', pipeline)

        # Get selected pipeline from YAML
        pipe: Pipeline_Block = self.etl_cfg.pipelines[pipeline]

        # Extract all sources
        dfs = [self._make('extractors', key).extract() for key in pipe.extractors]

        # Transform all extractions
        for df in dfs:
            for key in pipe.transformers:
                df = self._make('transformers', key).transform(df)

        # Load cleaned data
        for df in dfs:
            for key in pipe.loaders:
                self._make('loaders', key).load(df)
        
        # Log task finish
        log.info('Pipeline %s completed.', pipeline)

        return None

    # Method to be called to kickstart process, checks if task or pipeline for single or multiple runs.
    @log_exceptions
    def run(self, name: str) -> None:
        if name in self.etl_cfg.tasks:
            pipelines = self.etl_cfg.tasks[name].pipelines
            log.info('Task %s selected successfully.', name)
        elif name in self.etl_cfg.pipelines:
            pipelines = [name]
        else:
            raise ValueError(f'{name} task or pipeline name could not be found. Exiting without changes.')
        
        for pipe in pipelines:
            self._run_single_pipeline(pipe)

# EOF

if __name__ == '__main__':
    print('This module is intended to be imported, not run directly.')