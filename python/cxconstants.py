from os import makedirs as _make_dirs
from os.path import isdir as _isdir, join as _join

AUTHOR = 'CeroProgramming'
LICENSE = 'MIT'
VERSION = '0.0.1'
DATAFP = '/var/local/cxapps/'
LOGFP = '/var/log/cxapps/'
LOGFILENAME = 'default.log'
APPFP = '/usr/local/cxapps/'
APPSFP = '/usr/local/cxapps/modules/'
CONFIGFP = '/usr/local/etc/cxapps/'
LIBFP = '/usr/local/lib/cxlibs/'

LOG_LEVEL = 'DEBUG'
MODE = 'dev'

if MODE == 'dev':
    DATAFP = '/tmp' + DATAFP
    LOGFP = '/tmp' + LOGFP
    APPFP = '/tmp' + APPFP
    APPSFP = '/tmp' + APPSFP
    CONFIGFP = '/tmp' + CONFIGFP

for fp in (DATAFP, LOGFP, APPFP, APPSFP, CONFIGFP):
    if not _isdir(fp):
        _make_dirs(fp)

def get_application_install_path(name):
    return _join(APPSFP, name.lower())
