import os
import pytest

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


@pytest.mark.parametrize('package', [
    'dnsmasq',
])
def test_pkg_installed(host, package):
    package = host.package(package)

    assert package.is_installed


@pytest.mark.parametrize('service', [
    'dnsmasq'
])
def test_service_is_enabled(host, service):
    service = host.service(service)

    assert service.is_enabled


def test_config_exists(host):
    file = host.file('/etc/dnsmasq.conf')

    assert file.exists
    assert file.user == 'root'
    assert file.group == 'root'

    print(file.content)


def test_config_is_valid(host):
    cmd = host.run('dnsmasq --test --conf-file=/etc/dnsmasq.conf')

    assert not cmd.rc
