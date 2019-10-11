from cxperms import chk_perms
from cxlog import logger
from cxio import pip_package_exists

# Apt
if pip_package_exists('apt'):

    from apt.cache import Cache, LockFailedException
    from apt.progress import TextFetchProgress, InstallProgress

    # TODO fetch_progress?, LockFailedException

    @chk_perms
    def install(*package_names) -> None:

        upgrade()

        cache = Cache()
        cache.update()
        cache.open()

        for name in package_names:

            if name not in cache:
                logger.error('Package %s not found!' % (name,))
                continue

            package = cache[name]

            if package.is_installed:
                logger.warning('Package %s already installed!' % (name,))
                continue

            package.mark_install()

        cache.commit(TextFetchProgress(), InstallProgress())

        cache.close()


    @chk_perms
    def remove(*package_names) -> None:

        upgrade()

        cache = Cache()
        cache.update()
        cache.open()

        for name in package_names:

            if name not in cache:
                print('Package %s not found!' % (name,))
                continue

            package = cache[name]

            if not package.is_installed:
                print('Package %s is not installed!' % (name,))
                continue

            package.mark_delete(purge=True)

        cache.commit(TextFetchProgress(), InstallProgress())

        cache.close()


    @chk_perms
    def upgrade() -> None:

        cache = Cache()
        cache.update()
        cache.open()
        cache.update()
        cache.open()
        cache.upgrade(dist_upgrade=True)
        cache.fix_broken()
        cache.commit(TextFetchProgress(), InstallProgress())
        cache.close()
