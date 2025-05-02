# Import dependencies
import os, re

ENV_REF = re.compile(r'\$\{env:([A-Z0-9_]+)\}')

def expand_env(obj) -> dict:
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