# Import dependencies
import os
import re

ENV_REF = re.compile(r'\$\{env:([A-Z0-9_]+)\}')

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


# EOF

if __name__ == '__main__':
    print('This module is intended to be imported, not run directly.')