from collections import OrderedDict
from starmaker.ssh.core import SSHConfig
from starmaker.ssh.models import HostConfig
from starmaker.ssh.engine import SSHClient


def test_config_resolve_host():
    "Load default config and resolve host"
    config = SSHConfig.default()
    result = config.resolve_host('we-like-to-work')

    result.should.be.a(HostConfig)

    result.host_ip.should.equal("192.241.128.183")


def test_connect_id_ed25519():
    c = SSHClient()
    c.load_keys().should.be.none
    key = c.config.get_any_available_key()
    import ipdb;ipdb.set_trace()
