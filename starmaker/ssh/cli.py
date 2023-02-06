#!/usr/bin/env python3
import os
from pathlib import Path
from collections import OrderedDict

import click
from starmaker.ssh.core import SSHConfig
from starmaker.ssh.engine import SSHClient


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
    import ipdb;ipdb.set_trace()


@main.command()
@click.argument("host-name")
@click.argument("meta-args", nargs=-1)
@click.pass_context
def client(ctx, host_name, meta_args):
    path = Path("~/.ssh/config").expanduser()
    config = SSHConfig(path)
    ssh = SSHClient(config)
    import ipdb;ipdb.set_trace()
    keys = ssh.load_keys()
    import ipdb;ipdb.set_trace()
    sftp = ssh.establish_sftp(host_name, config=config)
    import ipdb;ipdb.set_trace()

if __name__ == "__main__":
    main()
