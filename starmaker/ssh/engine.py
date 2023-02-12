#!/usr/bin/env python3
import paramiko

from typing import Optional
from collections import OrderedDict
from starmaker.ssh.core import SSHConfig
from starmaker.ssh.models import HostConfig


class SFTP(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.authentication_errors = []
        self._connection = None
        self._sftp = None

    @property
    def connection(self):
        return self.get_connection()

    def get_connection(self):
        if not self._connection:
            self._connection = self.connect()

        return self._connection

    @property
    def sftp(self):
        return self.get_sftp()

    def get_sftp(self):
        if not self._sftp:
            self._sftp = paramiko.SFTPClient.from_transport(
                self.connection
            )

        return self._sftp

    def authenticate_transport(self, transport):
        transport.start_client()
        agent = paramiko.Agent()
        for key in agent.get_keys():
            try:
                transport.auth_publickey(self.user, key)
            except paramiko.SSHException as e:
                self.authentication_errors.append(e)

        return transport

    def create_transport(self, transport):
        transport = paramiko.Transport((self.host, int(self.port)))
        return transport

    def connect(self):
        t = self.create_transport()
        return self.authenticate_transport(t)

    def put(self, fd, destination):
        self.sftp.chdir(path=None)
        attributes = sftp.putfo(fd, destination, confirm=True)
        success = fd.tell() == attributes.st_size
        return success

    def get(self, fd, destination):
        # getfo(remotepath, fl, callback=None, prefetch=True)
        attributes = sftp.putfo(fd, destination, confirm=True)
        success = fd.tell() == attributes.st_size
        return success

    def ls(self, path='.'):
        items = self.sftp.list(path)
        return items


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
            raise

    def establish_sftp(self, host_name, config: Optional[SSHConfig] = None):
        conn = self.connect(host_name, config)
        sftp = self.sftp.get(host_name)
        if sftp is not None:
            raise SFTPSessionAlreadyEstablished(sftp)

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
