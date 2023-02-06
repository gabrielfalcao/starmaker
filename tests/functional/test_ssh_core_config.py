from paramiko.ed25519key import Ed25519Key

from starmaker.ssh.core import SSHConfig
from starmaker.ssh.models import HostConfig
from starmaker.ssh.engine import SSHClient


def test_config_resolve_host():
    "Load default config and resolve host"
    config = SSHConfig.default()
    result = config.resolve_host('we-like-to-work')

    result.should.be.a(HostConfig)

    result.host_ip.should.equal("192.241.128.183")


def test_client_connect_id_ed25519():
    c = SSHClient()

    key = c.config.get_any_available_key()
    key.should_not.be.none
    key.should.be.an(Ed25519Key)

    conn = c.connect('we-like-to-work')
    import ipdb;ipdb.set_trace()
