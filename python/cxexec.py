from cxperms import chk_perms
from cxlog import logger

from subprocess import run, PIPE, STDOUT


class FailedToExecute(Exception):
    def __init__(self, command, exit_code, error_output):
        error_message = 'The execution of the command \'%s\' returned error code %d. Stderr: \n%s' \
                        % (command, exit_code, error_output)
        logger.critical(error_message)
        super(FailedToExecute, self).__init__(error_message)


@chk_perms
def execute(command, code=True, combine=False, check=True, text=True, shell=True, onlycode=False, onlyerror=False):

    logger.info('Command %s gets executed.' % (command,))

    if combine:
        process = run(command, stdout=PIPE, stderr=STDOUT, text=text, shell=shell, executable='/bin/bash')
        logger.debug('Exit code: %s \nStdout: %s \nStderr: %s' % (process.returncode, process.stdout, process.stderr))
    else:
        process = run(command, capture_output=True, text=text, shell=shell, executable='/bin/bash')
        logger.debug('Exit code: %s \nStdout: %s' % (process.returncode, process.stdout))

    if check and process.returncode != 0:
        raise FailedToExecute(command, process.returncode, process.stderr)

    if onlycode:
        return process.returncode
    elif onlyerror:
        return process.stderr, process.returncode
    elif code and combine:
        return process.stdout, process.returncode
    elif code:
        return process.stdout, process.stderr, process.returncode
    elif combine:
        return process.stdout
    else:
        return process.stdout, process.stderr
