from cxconstants import LOGFP, LOGFILENAME, LOG_LEVEL
from socket import gethostname as _get_hostname, gethostbyname as _get_host_by_name

from os.path import join as _join
from logging import getLogger, Formatter, NOTSET, DEBUG, INFO, WARNING, ERROR, CRITICAL
from logging.handlers import TimedRotatingFileHandler
from inspect import stack
from datetime import time


class NoValidDebugLevel(Exception):
    def __init__(self):
        super().__init__('No valid debug level found. Choose between NOTSET, DEBUG, INFO, WARNING, ERROR, CRITICAL..')


class Logger(object):

    def __init__(self, logfp=None, logfilename=None, loglevel=None):

        if logfp: LOGFP = logfp
        if logfilename: LOGFILENAME = logfilename
        if loglevel: LOG_LEVEL = loglevel

        self.logger = getLogger()

        formatter = Formatter(fmt='%(asctime)s - %(levelname)s  - %(hostname)s:%(ip)s -  %(function)s - %(message)s',
                              datefmt='%d-%b-%y %H:%M:%S')

        file = TimedRotatingFileHandler(_join(LOGFP, LOGFILENAME), when='W6', atTime=time(2))
        file.setFormatter(formatter)

        self.context = {'ip':  _get_host_by_name(_get_hostname()), 'hostname': _get_hostname()}

        if LOG_LEVEL.upper() == 'NOTSET':
            file.setLevel(NOTSET)
        elif LOG_LEVEL.upper() == 'DEBUG':
            file.setLevel(DEBUG)
        elif LOG_LEVEL.upper() == 'INFO':
            file.setLevel(INFO)
        elif LOG_LEVEL.upper() == 'WARNING':
            file.setLevel(WARNING)
        elif LOG_LEVEL.upper() == 'ERROR':
            file.setLevel(ERROR)
        elif LOG_LEVEL.upper() == 'CRITICAL':
            file.setLevel(CRITICAL)
        else:
            raise NoValidDebugLevel()

        self.logger.addHandler(file)

    def debug(self, message):
        context = self.context.copy()
        context['function'] = stack()[1].function
        self.logger.debug(message, extra=context)

    def info(self, message):
        context = self.context.copy()
        context['function'] = stack()[1].function
        self.logger.info(message, extra=context)

    def warning(self, message):
        context = self.context.copy()
        context['function'] = stack()[1].function
        self.logger.warning(message, extra=context)

    def error(self, message):
        context = self.context.copy()
        context['function'] = stack()[1].function
        self.logger.error(message, extra=context)

    def critical(self, message):
        context = self.context.copy()
        context['function'] = stack()[1].function
        self.logger.critical(message, extra=context)


logger = Logger()
