# Import dependencies
from functools import wraps
# <INSERT PKG HERE FOR EXCEPTIONS>
import logging
log = logging.getLogger(__name__)


def pkg_error_handle(func):
    '''Error handler for all Github API issues.

    Args:
        func (Callable): Github API method being wrapped.

    Yields:
        Generator
    '''

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except BadCredentialsException as e:
            log.exception('Invalid credentials provided!')
            raise
        except BadAttributeException as e:
            log.exception('Wrong attribute type returned!')
            raise
        except RateLimitExceededException as e:
            log.exception('Rate limit exceeded!')
            raise
        except BadUserAgentException as e:
            log.exception('Request sent with bad user agent header.')
            raise
        except UnknownObjectException as e:
            log.exception('Request for non-existent object.')
            raise
        except TwoFactorException as e:
            log.exception('Onetime password for two-factor authentication required.')
            raise
        except GithubException as e:
            log.exception(f'API error (status {e.status}): {e.data}')
            raise RuntimeError(f'API error: {e.status}') from e

    return wrapper


# EOF

if __name__ == '__main__':
    print('This module is intended to be imported, not run directly.')