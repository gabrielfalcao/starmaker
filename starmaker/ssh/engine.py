#!/usr/bin/env python3
import paramiko

from typing import Optional
from collections import OrderedDict
from starmaker.ssh.core import SSHConfig
from starmaker.ssh.models import HostConfig


class EngineError(Exception):
    """raised by elements of :py:mod:``starmaker.ssh.engine``"""


class SFTPSessionNotEstablished(Exception):
    """captain fantastic"""


class SFTPSessionAlreadyEstablished(Exception):
    """captain fantastic"""


class SSHClient(object):
    def __init__(self, config: Optional[SSHConfig] = None):
        self.client = paramiko.SSHClient()
        self.config = config or SSHConfig.default()
        self.sftp = OrderedDict()

    def load_keys(self, hconfig: HostConfig):
        # XXX: load self.keys from keys of resolved hostconfig
        return self.client.load_system_host_keys(hconfig.id_file)

    def connect(self, host_name, config: Optional[SSHConfig] = None):
        if not config:
            config = self.config

        hconfig = config.resolve_host(host_name)
        self.load_keys(hconfig)
        try:
            return self.client.connect(
                hconfig.host_ip,
                username=hconfig.user,
                pkey=hconfig.id_file,
                sock=hconfig.proxy_cmd,
                look_for_keys=False,
            )
        except Exception as e:
            err = e
            import ipdb;ipdb.set_trace()
            raise

    def establish_sftp(self, host_name, config: Optional[SSHConfig] = None):
        conn = self.connect(host_name, config)
        sftp = self.sftp.get(host_name)
        if sftp is not None:
            raise SFTPSessionAlreadyEstablished(sftp)

        import ipdb;ipdb.set_trace()
        sftp = self.client.open_sftp()
        self.sftp[host_name] = sftp
        # sftp.get(remote_path, local_path)
        # sftp.close()
        return sftp

    def terminate_sftp(self, host_name, config: Optional[SSHConfig] = None):
        sftp = self.sftp.pop(host_name)
        if sftp is None:
            raise EngineError(f'sftp session not established with {host_name}')

        return sftp
