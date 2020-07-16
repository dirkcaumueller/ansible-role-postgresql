import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']
).get_hosts('all')


def test_hosts_file(host):
    f = host.file('/etc/hosts')

    assert f.exists
    assert f.user == 'root'
    assert f.group == 'root'


def test_postgresql_is_running(host):
    svc = host.service("postgresql-12")
    assert svc.is_running
    assert svc.is_enabled


def test_override_exists(host):
    f = host.file("/etc/systemd/system/postgresql-12.service.d/override.conf")
    assert f.exists


def test_override_contains_pgdata(host):
    f = host.file("/etc/systemd/system/postgresql-12.service.d/override.conf")
    assert f.contains("Environment=PGDATA=/customer/pgdata")
