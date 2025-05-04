# Import dependencies
from pydantic import BaseModel, Field
import yaml

# Custom libraries
from ext_lib import expand_env


class Component_Block(BaseModel):
    class_name:     str                     = Field(..., alias = 'class')
    params:         dict[str, str | None]   = Field(default_factory = dict)

class Pipeline_Block(BaseModel):
    extractors:     list[str]
    concat:         bool                    = Field(default = False, description = 'Concatenation boolean for extracted sources, found in pipeline.yml')
    transformers:   list[str]
    loaders:        list[str]

class Task_Block(BaseModel):
    pipelines:      list[str]

class ETL_Config(BaseModel):
    extractors:     dict[str, Component_Block]
    transformers:   dict[str, Component_Block]
    loaders:        dict[str, Component_Block]
    pipelines:      dict[str, Pipeline_Block]
    tasks:          dict[str, Task_Block]


    @classmethod
    def from_yaml(cls, path: str) -> 'ETL_Config':
        # Open main config YAML and expand ENV vars with actual vars
        raw_cfg = yaml.safe_load(open(path, 'r'))
        expanded_cfg = expand_env(raw_cfg)
        return cls.model_validate(expanded_cfg)

# EOF

if __name__ == '__main__':
    print('This module is intended to be imported, not run directly.')