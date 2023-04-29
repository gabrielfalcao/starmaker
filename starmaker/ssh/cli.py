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
from starmaker.ssh.ep import get_ssh_hosts_from_config
from starmaker.logging import get_logger


def here() -> Path:
    return Path(os.getcwd()).absolute()


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


# @main.command()
# @click.argument("host-name")
# @click.argument("meta-args", nargs=-1)
# @click.pass_context
# def client(ctx, host_name, meta_args):
#     path = Path("~/.ssh/config").expanduser()
#     config = SSHConfig(path)
#
#     hconfig = config.resolve_host(host_name)
#     ssh = SSHClient(config)
#     keys = ssh.load_keys(hconfig)
#
#     sftp = ssh.establish_sftp(host_name, config=config)


@main.command()
@click.argument("source")
@click.argument("destination")
@click.pass_context
def sync(ctx, source, destination):
    host_name, remote_path = destination.split(':', 1)

    path = Path("~/.ssh/config").expanduser()
    config = SSHConfig(path)

    hconfig = config.resolve_host(host_name)
    loaded = config.load_key(hconfig.id_file, interactive=False)

    ssh = SSHClient(config)
    keys = ssh.load_keys(hconfig)
    sftp = ssh.establish_sftp(host_name, config=config)



@main.group('list')
@click.pass_context
def list(ctx):
    pass


# https://gist.githubusercontent.com/gabrielfalcao/575927980e0ecdc72d483b6d69daf8ec/raw/7fffe0b4c2aae88aa7eaeaf7c73034e5cebc0108/brew.sh
@list.command()
@click.pass_context
def hosts(ctx):
    host_config_list: HostConfig.List = get_ssh_hosts_from_config()
    print(host_config_list.format_pretty_table())




    # https://gist.githubusercontent.com/gabrielfalcao/575927980e0ecdc72d483b6d69daf8ec/raw/7fffe0b4c2aae88aa7eaeaf7c73034e5cebc0108/brew.sh

if __name__ == "__main__":
    main()
