from cxlog import logger

from os import getuid
from functools import wraps

class PermissionError(Exception):
    pass

def chk_perms(func):
    @wraps(func)
    def call(*args, **kwargs):
        if getuid() != 0:
            logger.critical('Program was called without root privileges!')
        #    raise PermissionError('This program is not run as sudo or root. Exiting..')
        result = func(*args, **kwargs)
        return result
    return call

def chk_perms_raw():
    if getuid() != 0:
        logger.critical('Program was called without root privileges!')
    #    raise PermissionError('This program is not run as sudo or root. Exiting..')
    pass
