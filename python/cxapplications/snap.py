from cxperms import chk_perms
from cxexec import execute
from cxlog import logger
from cxio import command_exists

if command_exists('snap'):

    @chk_perms
    def install(*package_names) -> None:

        for name in package_names:

            logger.info('Installing snap package %s' % (name,))
            if execute('snap info %s' % (name,), onlycode=True) != 0:
                logger.error('Snap package %s not found!' % (name,))
                continue

            if name in list_all():
                logger.warning('Snap package %s already installed!' % (name,))
                continue

            err, code = execute('snap install %s' % (name,), check=False, onlyerror=True)
            if code != 0:
                logger.error('Snap package %s cannot be installed (exited with %s). Stderr:\n%s' % (name, code, err))


    @chk_perms
    def remove(*package_names) -> None:

        for name in package_names:

            logger.info('Removing snap package %s' % (name,))
            if execute('snap info %s' % (name,), onlycode=True) != 1:
                logger.error('Snap package %s not found!' % (name,))
                continue

            if name not in list_all():
                logger.warning('Snap package %s not installed!' % (name,))
                continue

            err, code = execute('snap remove %s' % (name,), check=False, onlyerror=True)
            if code != 0:
                logger.error('Snap package %s cannot be removed (exited with %s). Stderr:\n%s' % (name, code, err))


    @chk_perms
    def list_all() -> list:
        packages_raw = execute('snap list', combine=True, code=False)
        packages_pre = packages_raw.rsplit('\n')[1:-1]
        packages_post = [e[0:e.find(' ')] for e in packages_pre]
        return packages_post


    @chk_perms
    def upgrade() -> None:
        logger.info('Upgrading snap packages')
        err, code = execute('snap refresh', onlyerror=True)
        if code != 0:
            logger.error('Cannot upgrade snap packages (exited with %s). Stderr:\n%s' % (code, err))
