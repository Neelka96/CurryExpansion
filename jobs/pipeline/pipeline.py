# Import dependencies
from typing import overload, Literal
from importlib import import_module
import pandas as pd
import yaml

# Allow logging from top-level
import logging
log = logging.getLogger(__name__)

# Custom Libraries
from ext_lib import BaseExtractor, BaseTransformer, BaseLoader, expand_env
from yaml_stubs import Component_Config, Pipeline_Def, ETL_Config


class Pipeline_Runner:
    cfg: ETL_Config
    '''
    The Pipeline Runner is an abstraction of the ETL process meant to be orchestrated from the pipeline.yml file.  
    The top-level parent file that creates an instantiation must load in environment variables first via `dotenv.load_dotenv()` to ensure they're expanded properly.
    After instantiation, execute method `.run(YOUR_PIPELINE_NAME_HERE)` to run a specific pipeline in the yaml.

    :param config_path: String path where pipeline.yml lives.
    :type config_path: str
    
    :returns: Abstracted Pipeline containing the parsed yaml. Ready for specific pipeline execution.
    :rtype: Pipeline_Runner
    '''
    def __init__(self, config_path: str):
        # Open main config YAML and expand ENV vars with actual vars
        raw_cfg = yaml.safe_load(open(config_path, 'r'))
        expanded_cfg = expand_env(raw_cfg)
        self.cfg = ETL_Config.model_validate(expanded_cfg)
    
    # Type checks implementation for each component type and its corresponding base ETL part
    @overload
    def __make(self, component_type: Literal['extractors'],     name: str) -> BaseExtractor: ...
    @overload
    def __make(self, component_type: Literal['transformers'],   name: str) -> BaseTransformer: ...
    @overload
    def __make(self, component_type: Literal['loaders'],        name: str) -> BaseLoader: ...

    # Actual function definition with all variations
    def __make(self, component_type: Literal['extractors', 'transformers', 'loaders'], name: str) -> BaseExtractor | BaseTransformer | BaseLoader:
        '''Constructs an instance of a designated class with loaded parameters from the pipeline.yml.

        :param component_type: Specific section of pipeline building blocks.
        :type component_type: Literal[&#39;extractors&#39;, &#39;transformers&#39;, &#39;loaders&#39;]
        :param name: The title of the exact block to grab.
        :type name: str

        :returns: Always returns one of three base ETL object classes, linked to real classes in the ETL/ files.
        :rtype: BaseExtractor or BaseTransformer or BaseLoader
        '''
        # Gets the actual class specified by the YAML for pipeline and construct with paramaters
        comp_cfg: Component_Config = getattr(self.cfg, component_type)[name]
        module_name, cls_name = comp_cfg.class_name.rsplit('.', 1)
        Impl = getattr(import_module(module_name), cls_name)
        log.debug('Crafting import %s.%s.', (module_name, cls_name))
        return Impl(**(comp_cfg.params or {}))

    # Execution for pipeline begins and ends here
    def run(self, pipeline_name: str):
        '''Actual runtime with parsed class creation and pipeline execution.

        :param pipeline_name: Pipeline name from pipeline.yml to run.
        :type pipeline_name: str

        :returns: No return for success. See logging file for details.
        :rtype: None
        '''
        # Log pipeline start
        log.info('Pipeline %s started.', pipeline_name)

        # Get selected pipeline from YAML
        pipe: Pipeline_Def = self.cfg.pipelines[pipeline_name]

        # Extract all sources
        dfs = [self.__make('extractors', key).extract() for key in pipe.extractors]

        # Checks for merging requirement
        if pipe.merge: dfs = [pd.concat(dfs, ignore_index = True)]

        # Transform all extractions
        for df in dfs:
            for key in pipe.transformers:
                df = self.__make('transformers', key).transform(df)

        # Load cleaned data
        for df in dfs:
            for key in pipe.loaders:
                self.__make('loaders', key).load(df)
        
        # Log task finish
        log.info('Pipeline %s completed.', pipeline_name)

        return None


# EOF

if __name__ == '__main__':
    print('This module is intended to be imported, not run directly.')