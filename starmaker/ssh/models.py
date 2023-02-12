#!/usr/bin/env python3
from typing import Optional
from typing import NewType
from pathlib import Path
from collections import OrderedDict

import paramiko
from uiclasses.base import Model


KEY_CLASSES_BY_TYPE_NAME = (
    ("ed25519", paramiko.Ed25519Key),
    ("ecdsa", paramiko.ECDSAKey),
    ("rsa", paramiko.RSAKey),
)


class SSSHError(RuntimeError, IOError):
    """:py:class:``starmaker.ssh.models.StarmakerSSHError``"""


StarmakerSSHError = SSSHError


class ConfigError(StarmakerSSHError):
    """base exception for config-related stuff"""


class InvalidKey(StarmakerSSHError):
    """base exception for key-related stuff"""


class PrivateKeyFileDoesNotExist(InvalidKey):
    """raised when no SSH key private file exists (as a file)"""


class RequiresInteractive(InvalidKey):
    """raised when key requires password but interactive is ``False``"""


class InvalidREPLCallback(InvalidKey, ConfigError):
    """raised when a ``repl_getpass_callback`` arg is not callable"""


HostConfig = NewType("HConfig", Model)


class HostConfig(Model):

    name: str
    id_file: Path
    host_ip: str
    user: Optional[str]
    port: Optional[int]
    proxy_cmd: Optional[paramiko.ProxyCommand]

    @classmethod
    def from_paramiko_ssh_config_dict(
            cls, name: str, hconfig: paramiko.config.SSHConfigDict
    ) -> Optional[HostConfig]:
        hostname = hconfig.pop("hostname", name)

        # if not hostname or len(hconfig) == 1:
        #     return None

        kwargs = OrderedDict()
        kwargs["name"] = name
        kwargs["host_ip"] = hostname

        if "port" in hconfig:
            kwargs["port"] = int(hconfig["port"])

        if "user" in hconfig:
            kwargs["user"] = hconfig["user"]

        if "identityfile" in hconfig:
            t = next(iter(hconfig["identityfile"] or []), None)
            id_file = Path(t)
            if not id_file.is_file():
                raise PrivateKeyFileDoesNotExist(t)
            kwargs["id_file"] = id_file

        if "proxycommand" in hconfig:
            proxy_cmd = hconfig["proxycommand"]
            if proxy_cmd is not None:
                kwargs["proxy_cmd"] = paramiko.ProxyCommand(proxy_cmd)

        return cls(**kwargs)
