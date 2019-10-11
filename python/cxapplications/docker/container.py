from cxperms import chk_perms
from cxlog import logger
from cxio import pip_package_exists, sleep

if pip_package_exists('docker'):

    from docker import from_env as get_client
    from docker.models.images import Image
    from docker.models.containers import Container


@chk_perms
def get(name):
    return get_client().containers.get(name)


@chk_perms
def run(image_name, name, detach=True, **kwargs) -> Container:
    logger.info('Run a container with name %s from image %s' % (name, image_name))
    try:
        container = get_client().containers.run(image_name, name=name, detach=detach, **kwargs)
        if container.status !=



@chk_perms
def create(image_name, name, detach=True, **kwargs):
    logger.info('Create a container with name %s from image %s' % (name, image_name))
    container =  get_client().containers.create(image_name, name=name, detach=detach, **kwargs)


@chk_perms
def start(*container_names) -> None:
    logger.info('Starting containers: ' % (name, image_name))
    [get_client().containers.get(name).start() for name in container_names]


@chk_perms
def restart(*container_names, timeout=30) -> None:
    [get_client().containers.get(name).restart(timeout=timeout) for name in container_names]


@chk_perms
def stop(*container_names, timeout=30) -> None:
    [get_client().containers.get(name).stop(timeout=timeout) for name in container_names]


@chk_perms
def rm(*container_names, timeout=30):
    for name in container_names:
        container = get_client().containers.get(name)
        container.stop(timeout=timeout)
        container.remove()


@chk_perms
def prune() -> dict:
    return get_client().containers.prune()


@chk_perms
def pause(*container_names) -> None:
    [get_client().containers.get(name).pause() for name in container_names]


@chk_perms
def resume(*container_names) -> None:
    [get_client().containers.get(name).unpause() for name in container_names]


@chk_perms
def status(name) -> str:
    return get_client().containers.get(name).status()


@chk_perms
def list(raw=False) -> list:
    if raw:
        return get_client().containers.list()
    else:
        return [container.name for container in get_client().containers.list()]


@chk_perms
def stats(*container_names) -> list:
    return [get_client().containers.get(name).stats(stream=True, decode=True) for name in container_names]


@chk_perms
def exec_inside(name, command, sudo=False, user='root', detach=True, stream=True) -> tuple:
    return get_client().containers.get(name).exec_run(cmd=command, privileged=sudo, user=user, stream=stream,
                                                      detach=detach)


@chk_perms
def export(name, fp, chunk_size=2097152) -> None:
    bits, status = get_client().containers.get(name).export(chunk_size=chunk_size)
    with open(fp, 'wb') as f:
        for chunk in bits:
            f.write(chunk)
