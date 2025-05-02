from pydantic import BaseModel, Field

class Component_Config(BaseModel):
    class_name:     str                     = Field(..., alias = 'class')
    params:         dict[str, str | None]   = Field(default_factory = dict)

class Pipeline_Def(BaseModel):
    extractors:     list[str]
    merge:          bool                    = Field(default = False, description = 'Merge boolean for extracted sources, found in pipeline.yml')
    transformers:   list[str]
    loaders:        list[str]

class ETL_Config(BaseModel):
    extractors:     dict[str, Component_Config]
    transformers:   dict[str, Component_Config]
    loaders:        dict[str, Component_Config]
    pipelines:      dict[str, Pipeline_Def]


# EOF

if __name__ == '__main__':
    print('This module is intended to be imported, not run directly.')