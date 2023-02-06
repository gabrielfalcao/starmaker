#!/usr/bin/env python3
import os
from pathlib import Path
from collections import OrderedDict

import click
import logging
from starmaker.ssh.core import SSHConfig
from starmaker.ssh.models import HostConfig
from starmaker.ssh.models import StarmakerSSHError
from starmaker.ssh.engine import SSHClient


def here() -> Path:
    return Path(os.getcwd()).absolute()


def get_logger():
    logger = logging.getLogger(__name__)
    logger.addHandler(logging.NullHandler())
    return logger


@click.group()
@click.option("--debug/--no-debug", default=False)
@click.pass_context
def main(ctx, debug):
    ctx.obj = OrderedDict(debug=debug, cwd=here())


@main.command()
@click.argument("host-name", nargs=1)
@click.pass_context
def conf(ctx, host_name):
    path = Path("~/.ssh/config").expanduser()
    sshconf = SSHConfig(path)
    hconfig = sshconf.resolve_host(host_name)
    import ipdb

    ipdb.set_trace()


@main.command()
@click.argument("host-name")
@click.argument("meta-args", nargs=-1)
@click.pass_context
def client(ctx, host_name, meta_args):
    path = Path("~/.ssh/config").expanduser()
    config = SSHConfig(path)
    ssh = SSHClient(config)
    keys = ssh.load_keys()

    sftp = ssh.establish_sftp(host_name, config=config)
    import ipdb;ipdb.set_trace()


@main.command()
@click.pass_context
def list(ctx):
    path = Path("~/.ssh/config").expanduser()
    config = SSHConfig(path)
    hosts = []

    logger = get_logger()

    for host_name in config.conf.get_hostnames():
        try:
            resolved = config.resolve_host(host_name)
            hosts.append(resolved)

        except StarmakerSSHError as e:
            logger.exception(f"failed to resolve host {host_name}: {e}")

    hosts = HostConfig.List(filter(lambda x: bool(x) and x.name != '*', hosts))
    print(hosts.format_pretty_table())


if __name__ == "__main__":
    main()
