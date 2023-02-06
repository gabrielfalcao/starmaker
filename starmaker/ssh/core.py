#!/usr/bin/env python3
import paramiko
import getpass
from typing import Optional, Callable
from pathlib import Path

from starmaker.ssh.models import HostConfig


def resolve_key_path(key_filename: Path) -> Path:
    return key_filename.expanduser().relative_to(Path("~").expanduser())


class ConfigError(IOError):
    """base exception for config-related stuff"""


class InvalidKey(IOError):
    """base exception for key-related stuff"""


class PrivateKeyFileDoesNotExist(InvalidKey):
    """raised when no SSH key private file exists (as a file)"""


class RequiresInteractive(InvalidKey):
    """raised when key requires password but interactive is ``False``"""


class InvalidREPLCallback(InvalidKey, ConfigError):
    """raised when a ``repl_getpass_callback`` arg is not callable"""


class SSHConfigTranslator(object):
    def __init__(self, config: paramiko.config.SSHConfigDict):
        self.source = config


class REPLUI(object):
    def __init__(self, interactive: bool = False, repl_getpass_callback: Callable):
        if not callable(repl_getpass_callback):
            raise InvalidREPLCallback(
                f'{repl_getpass_callback} is not callable')

        self.repl_getpass_callback = repl_getpass_callback
        self.interactive = interactive

    def get_keypass(self, key_filename: Path) -> Optional[str]:
        if self.interactive:
            return self.repl_getpass_callback(
                f"enter password for key '{key_filename}'")

    def error_password_required(self, key_filename: Path) -> InvalidKey:
        raise RequiresInteractive(
            f"the key file {key_filename} requires password but "
            "the -i argument was not properly provided"
        )


class SSHConfig(object):
    __key_classes_by_type_name__ = (
        ('ed25519', paramiko.Ed25519Key),
        ('ecdsa', paramiko.ECDSAKey),
        ('rsa', paramiko.RSAKey),
    )

    def __init__(self, ssh_config_path: Path):
        if not isinstance(ssh_config_path, Path):
            raise TypeError(f'{ssh_config_path} is not a pathlib.Path')

        try:
            self.fstat = ssh_config_path.stat()
        except FileNotFoundError:
            raise ConfigError(f'``{ssh_config_path}`` does not exist')

        if not ssh_config_path.is_file():
            raise ConfigError(f'{ssh_config_path} is not a file')

        self.conf = paramiko.SSHConfig()
        with ssh_config_path.open(encoding='utf-8') as fd:
            self.conf.parse(fd)

        self.config_path = ssh_config_path
        self.interactive_callback = getpass.getpass
        self.path = ssh_config_path.parent

    @classmethod
    def default(cls):
        path = Path("~/.ssh/config").expanduser()
        return cls(path)

    def resolve_host(self, name: str) -> Optional[HostConfig]:
        hconfig = self.conf.lookup(name)
        return HostConfig.from_paramiko_ssh_config_dict(hconfig)

    def load_key(self, key_filename: Path, interactive: bool = False):
        for (kname, ktype) in self.__key_classes_by_type_name__:
            keypass = None
            if kname in key_filename.name:
                if interactive:
                    keypass = REPLUI(self.interactive_callback, interactive).get_keypass(key_filename)

                try:
                    pkey = ktype.from_private_key_file(key_filename, keypass)
                except paramiko.PasswordRequiredException:
                    raise REPLUI(interactive).error_password_required(
                        key_filename)

                return pkey

        raise InvalidKey(f'Failed to load private key: {key_filename}')

    def yield_any_available_key(self):
        for (kname, ktype) in self.__key_classes_by_type_name__:
            possible_name = Path(f'~/.ssh/id_{kname}')
            if possible_name.is_file():
                yield self.load_key(possible_name)

    def get_any_available_key(self):
        for key in self.yield_any_available_key():
            if key:
                return key
