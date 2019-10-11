from cxperms import chk_perms
from cxexec import execute
from cxlog import logger

from os import makedirs as _make_dirs, chmod as _chmod
from os.path import isdir as _isdir, join as _join
from shutil import copy as _copy, move as _move
from time import sleep as _sleep
from socket import gethostname as _get_hostname, gethostbyname as _get_host_by_name
from importlib.util import find_spec as _find_spec
# from inspect import getmodulename, isfunction


@chk_perms
def make_all_dirs(*file_paths):
    for fp in file_paths:
        if not _isdir(fp):
            _make_dirs(fp)


@chk_perms
def copy(source, destination):
    _copy(source, destination)
    logger.info('Copied %s to %s' % (source, destination))


@chk_perms
def move(source, destination):
    _move(source, destination)
    logger.info('Move %s to %s' % (source, destination))


@chk_perms
def join(path, *suffix) -> str:
    return _join(path, *suffix)


@chk_perms
def change_mod(fp, mode):
    _chmod(fp, mode)
    logger.info('Changed mod for %s to %s' % (fp, mode))


@chk_perms
def change_mod_conjugated(fp, subfp, mode):
    _chmod(_join(fp, subfp), mode)
    logger.info('Changed mod for %s to %s' % (_join(fp, subfp), mode))


@chk_perms
def extract_tar(source, destination, mode):
    logger.warning('extract_tar not yet implemented.')
    pass


@chk_perms
def create_tar(source, destination, mode):
    logger.warning('create_tar not yet implemented.')
    pass


@chk_perms
def sleep(timeout):
    _sleep(timeout)


@chk_perms
def get_hostname() -> str:
    return _get_hostname()


@chk_perms
def get_host_ip() -> str:
    return _get_host_by_name(_get_hostname())


@chk_perms
def pip_package_exists(name) -> bool:
    if _find_spec(name):
        return True
    else:
        return False


@chk_perms
def command_exists(name) -> bool:
    if execute('command -v %s' % (name,), check=False, onlycode=True) == 0:
        return True
    else:
        return False


'''
me = __import__(getmodulename(__file__))
for name in dir(me):
    obj = getattr(me, name)
    if isfunction(obj):
        obj.__func__ = chk_perms(obj)
'''
