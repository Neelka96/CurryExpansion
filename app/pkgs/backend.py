# Import dependencies
from flask import request

# Bring in custom logger
from Core.log_config import init_log
log = init_log(__name__)

# Automatic Metadata Creation
def forge_metadata(
        route: str
        ,length: int
        ,desc: str
        ,params: dict
        ) -> dict:
    '''Helps create JSON via function passing.

    Args:
        route (str): API call route.
        length (int): Length of returned JSON.
        desc (str): API description.
        params (dict): Parameters passed in API call.

    Returns:
        dict: Inner metadata nest.
    '''
    log.debug('Inner wrapper for forge_json called.')
    return {
        'current_route': route
        ,'home_route': request.host
        ,'data_points': length
        ,'info': desc or None
        ,'params': params or {}
        ,'format': 'json'
    }

# Nests metadata and results together in one object 
def forge_json(
        route: str
        ,nest: dict
        ,desc: str
        ,params: dict | None = None
        ) -> dict:
    '''Completes full JSON-esque packaging.

    Args:
        route (str): API call route.
        nest (dict): Returned JSON.
        desc (str): API description.
        params (dict | None, optional): Parameters passed in API call. Defaults to None.

    Returns:
        dict: Full python style JSON ready for Flask export.
    '''
    log.debug('Creating custom JSON Metadata.')
    json_api = {
        'metadata': forge_metadata(route, len(nest), desc, params)
        ,'results': nest
    }
    return json_api


# EOF

if __name__ == '__main__':
    print('This module is intended to be imported, not run directly.')