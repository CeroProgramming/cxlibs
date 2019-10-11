from cxperms import chk_perms
from cxlog import logger
from cxio import pip_package_exists

if pip_package_exists('docker'):

    from docker import from_env as get_client
    from docker.models.images import Image
    from docker.errors import BuildError, ImageNotFound

    @chk_perms
    def get(name) -> Image:
        try:
            return get_client().images.get(name)
        except ImageNotFound:
            logger.error('Image %s not found..' % (name,))


    @chk_perms
    def build(fp, tag, logs=False, remove=True, timeout=300, pull_image=True, **kwargs):
        logger.info('Building image %s from %s' % (tag, fp))
        try:
            image, log = get_client().images.build(path=fp, tag=tag, rm=remove, timeout=timeout, pull=pull_image,
                                                   **kwargs)
            if logs:
                return (image, log)
            else:
                return image
        except BuildError:
            logger.error('Build for image from %s failed' % (fp,))


    @chk_perms
    def pull(name, tag='latest', **kwargs) -> Image:
        logger.info('Pulling image %s' % (name,) if not tag else 'Pulling image %s:%s' % (name, tag))
        image = get_client().images.pull(name, tag=tag, **kwargs)
        if type(image) == list():
            return image[0]
        return image


    @chk_perms
    def save(name, fp, chunk_size=2097152, named=True) -> None:
        logger.info('Saving image %s to file %s' % (name, fp))
        with open(fp, 'wb') as f:
            for e in get_client().images.get(name).save(chunk_size=chunk_size, named=named):
                f.write(e)


    @chk_perms
    def load(fp) -> list:
        with open(fp, 'rb') as f:
            images = get_client().images.load(f)
        return images


    @chk_perms
    def rm(*image_names, **kwargs) -> list:
        [get_client().images.remove(image=name, **kwargs) for name in image_names]


    @chk_perms
    def prune() -> dict:
        return get_client().images.prune()


    @chk_perms
    def list_all(name=True, raw=False, **kwargs) -> list:
        if name:
            return [image.name for image in get_client().images.list(**kwargs)]
        elif raw:
            return get_client().images.list()
