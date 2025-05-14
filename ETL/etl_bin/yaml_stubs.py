# Import dependencies
from pydantic import BaseModel, Field
import yaml, os, re

ENV_REF = re.compile(r'\$\{env:([A-Za-z0-9_]+)\}')

def expand_env(obj) -> dict:
    '''Recursive expansion of python object for inserting environment variables.
    Please wrap with error handling. Function will just return unexpandable objects in current form.

    :param obj: Expects dict, list, or str.
    :type obj: Any

    :returns: An object expanded for environment variables - typically a YAML
    :rtype: dict
    '''
    if isinstance(obj, dict):
        return {k: expand_env(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [expand_env(v) for v in obj]
    if isinstance(obj, str):
        m = ENV_REF.match(obj)
        if m:
            return os.getenv(m.group(1))
    return obj


class YamlComponents(BaseModel):
    class_name:     str                         = Field(..., alias = 'class')
    params:         dict[str, int | str | None] = Field(default_factory = dict)

class YamlPipelines(BaseModel):
    extractors:     list[str]
    transformers:   list[str]
    loaders:        list[str]

class YamlTasks(BaseModel):
    pipelines:      list[str]

class YamlETL(BaseModel):
    extractors:     dict[str, YamlComponents]
    transformers:   dict[str, YamlComponents]
    loaders:        dict[str, YamlComponents]
    pipelines:      dict[str, YamlPipelines]
    tasks:          dict[str, YamlTasks]


    @classmethod
    def from_yaml(cls, path: str) -> 'YamlETL':
        # Open main config YAML and expand ENV vars with actual vars
        raw_cfg = yaml.safe_load(open(path, 'r'))
        expanded_cfg = expand_env(raw_cfg)
        return cls.model_validate(expanded_cfg)

# EOF

if __name__ == '__main__':
    print('This module is intended to be imported, not run directly.')