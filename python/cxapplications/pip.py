from cxperms import chk_perms
from cxexec import execute
from cxlog import logger


@chk_perms
def install(*package_names) -> None:
    for name in package_names:
        logger.info('Installing pip package %s' % (name,))
        err, code = execute('python3 -m pip install --upgrade %s' % (name,), check=False, onlyerror=True)
        if code != 0:
            logger.error('Pip package %s cannot be installed. Stderr:\n%s' % (name, err))


@chk_perms
def remove(*package_names) -> None:
    for name in package_names:
        logger.info('Removing pip package %s' % (name,))
        err, code = execute('python3 -m pip uninstall %s' % (name,), check=False, onlyerror=True)
        if code != 0:
            logger.error('Pip package %s cannot be removed. Stderr:\n%s' % (name, err))


@chk_perms
def list_all() -> list:
    packages_raw = execute('python3 -m pip list', combine=True, code=False)
    packages_pre = packages_raw.rsplit('\n')[2:-1]
    packages_post = [e[0:e.find(' ')] for e in packages_pre]
    return packages_post


@chk_perms
def upgrade() -> None:
    logger.info('Upgrading pip packages')
    install(*list_all())
