import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']
).get_hosts('all')


def test_ram_disk(host):
    m = host.mount_point('/var/lib/pgsql/12/data/pg_stat_tmp')

    assert m.exists
    assert m.filesystem == 'tmpfs'


def test_postgresql_is_running(host):
    svc = host.service("postgresql-12")
    assert svc.is_running
    assert svc.is_enabled
