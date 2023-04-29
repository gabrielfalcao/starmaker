from pathlib import Path
from starmaker.ssh.core import SSHConfig
from starmaker.ssh.models import HostConfig
from starmaker.ssh.models import StarmakerSSHError
from starmaker.ssh.engine import SSHClient
from starmaker.ssh.engine import SFTP
from starmaker.logging import get_logger


def get_ssh_hosts_from_config(location: str="~/.ssh/config", ignore_names: tuple = ('*')):
    path = Path(location).expanduser()
    config = SSHConfig(path)
    hosts = []

    logger = get_logger()

    for host_name in config.conf.get_hostnames():
        try:
            resolved = config.resolve_host(host_name)
            hosts.append(resolved)

        except StarmakerSSHError as e:
            logger.exception(f"failed to resolve host {host_name}: {e}")

    return HostConfig.List(filter(lambda x: bool(x) and x.name not in ignore_names, hosts))
