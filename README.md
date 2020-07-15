# Ansible Role: PostgreSQL

[![Build Status](https://travis-ci.org/dirkcaumueller/postgresql.svg?branch=master)](https://travis-ci.org/dirkcaumueller/ansible-role-postgresql)

Installs and configures PostgreSQL v12 server on RHEL/CentOS servers.

## Requirements

No special requirements; note that this role requires root access, so either run it in a playbook with a global `become: yes`, or invoke the role in your playbook like:

    - hosts: database
      roles:
        - role: dirkcaumueller.postgresql
          become: yes

## Role Variables

Available variables are listed below, along with default values (see `defaults/main.yml`):

```yml
---
# Set PostgreSQL type
# pg - Community PostgreSQL (default)
# edb - EnterpriseDB PostgreSQL Advanced Server
pg_type: pg

# Set major version of PostgreSQL
pg_major_version: 12

# Create a master or standby PostgreSQL instance
pg_cluster_type: master

# PostgreSQL Development Group Yum repository
pg_repo_url: "https://download.postgresql.org/pub/repos/yum/reporpms/EL-7-x86_64/pgdg-redhat-repo-latest.noarch.rpm"
pg_enablerepo: "pgdg12"

# Packages to install for PostgreSQL
pg_packages:
  - postgresql{{ pg_major_version }}-server
  - postgresql{{ pg_major_version }}-contrib
  - postgresql{{ pg_major_version }}-libs
  - postgresql{{ pg_major_version }}
  - pg_top

# Package for Python to administer PostgreSQL
pg_python_libraries:
  - python-psycopg2
  - python-passlib

# PostgreSQL OS user and group
pg_user: postgres
pg_user_password: ""
pg_group: postgres

# PostgreSQL database cluster superuser
pg_superuser: postgres
pg_superuser_password: ""

# Required & optional directories
pg_user_home: "/var/lib/pgsql"
pg_data_dir: "/var/lib/pgsql/{{ pg_major_version }}/data"
pg_bin_path: "/usr/pgsql-{{ pg_major_version }}/bin"
pg_log_dir: ""
pg_wal_archive_dir: ""

# Make ${PGDATA}/pg_stat_tmp a RAM-disk (false/true) with defined size
pg_stat_tmp_on_ram_disk: false
pg_stat_tmp_ram_size: "128m"

# PostgreSQL port
pg_port: 5432

# PostgreSQL service
pg_service: postgresql-{{ pg_major_version }}
pg_service_state: started
pg_service_enabled: true

# Set postgresql state when configuration changes are made. Recommended values:
# 'restarted' or 'reloaded'
pg_restarted_state: restarted

# PostgreSQL environment variables
pg_env_vars:
  - "PATH=/usr/pgsql-{{ pg_major_version }}/bin:$PATH"
  - "LD_LIBRARY_PATH=/usr/pgsql-{{ pg_major_version }}/lib:$LD_LIBRARY_PATH"
  - "PGLOCALEDIR=/usr/pgsql-{{ pg_major_version }}/share/locale"
  - "PGDATA={{ pg_data_dir }}"

# Directory for UNIX sockets
pg_unix_socket_directories:
  - /var/run/postgresql

# Configure parameters for cluster initialization
pg_initdb_params: "--encoding=UTF8 --locale=en_US.UTF-8 --lc-collate=C --lc-ctype=C --data-checksums"

# Host based authentication (hba) entries to be added to the pg_hba.conf; this
# variable's defaults reflect the defaults that come with a fresh installation
pg_hba_entries:
  - {type: local, database: all, user: all, address: null, auth_method: peer, state: present}
  - {type: host, database: all, user: all, address: '127.0.0.1/32', auth_method: md5, state: present}
  - {type: host, database: all, user: all, address: '::1/128', auth_method: md5, state: present}
  - {type: local, database: replication, user: all, address: null, auth_method: peer, state: present}
  - {type: host, database: replication, user: all, address: '127.0.0.1/32', auth_method: md5, state: present}
  - {type: host, database: replication, user: all, address: '::1/128', auth_method: md5, state: present}

# Global configuration options that will be set via ALTER SYSTEM in postgresql.auto.conf
pg_postgresql_conf_params: []
#  - name:
#    value:

# Add databases to cluster
pg_databases: []
# - name: exampledb # required; the rest are optional
#   lc_collate: # defaults to 'en_US.UTF-8'
#   lc_ctype: # defaults to 'en_US.UTF-8'
#   encoding: # defaults to 'UTF-8'
#   template: # defaults to 'template0'
#   login_host: # defaults to 'localhost'
#   login_password: # defaults to not set
#   login_user: # defaults to '{{ pg_user }}'
#   login_unix_socket: # defaults to 1st of '{{ pg_unix_socket_directories }}'
#   port: # defaults to not set
#   owner: # defaults to '{{ pg_user
#   state: # defaults to 'present'

# Add users to cluster
pg_users: []
# - name: jdoe # required; the rest are optional
#   password: # defaults to not set
#   encrypted: # defaults to not set
#   role_attr_flags: # defaults to not set
#   db: # defaults to not set
#   login_host: # defaults to 'localhost'
#   login_password: # defaults to not set
#   login_user: # defaults to '{{ pg_user }}'
#   login_unix_socket: # defaults to 1st of '{{ pg_unix_socket_directories }}'
#   port: # defaults to not set
#   state: # defaults to 'present'
#
# - name: replicator # Role for streaming replication
#   password: replicator_password
#   role_attr_flags: REPLICATION
#   db: postgres
#   login_user: "{{ pg_user }}""
#   state: present

# Add extensions to databases
pg_extensions: []
#  - name: pg_stat_statements # required
#    version: # defaults to 'latest'
#    db: postgres # required
#    schema: # defaults to not set
#    cascade: # defaults to 'no'
#    login_host: # defaults to 'localhost'
#    login_password: # defaults to not set
#    login_user: # defaults to '{{ pg_user }}'
#    login_unix_socket: # defaults to 1st of '{{ pg_unix_socket_directories }}'
#    port: # defaults to not set
#    state: present # defaults to 'present'

# Add existing roles of db cluster to .pgpass file; password taken from pg_shadow
pg_pass_roles: []
#  - name: replicator
#    hostname: "*"
#    port: "{{ pg_port }}"
#    database: replication
```

Some additional variables for EDB's Postgres Advanced Server (WIP).

```yml
---
# EnterpriseDB Yum repository url
pg_repo_url: "http://yum.enterprisedb.com/edbrepos/edb-repo-latest.noarch.rpm"
pg_enablerepo: "edb"
# edb_yum_username: ""
# edb_yum_password: ""

# Packages to install for PostgreSQL
pg_packages:
  - edb-as{{ pg_major_version }}-server
  - edb-as{{ pg_major_version }}-server-core
  - edb-as{{ pg_major_version }}-server-edb-modules
  - edb-as{{ pg_major_version }}-server-contrib
  - edb-as{{ pg_major_version }}-server-libs
  - edb-as{{ pg_major_version }}-server-client
  - edb-as{{ pg_major_version }}-server-llvmjit
  - edb-as{{ pg_major_version }}-server-sslutils
  - edb-as{{ pg_major_version }}-server-indexadvisor
  - edb-as{{ pg_major_version }}-server-sqlprofiler
  - edb-as{{ pg_major_version }}-server-sqlprotect

# EnterpriseDB OS user and group
pg_user: enterprisedb
pg_group: enterprisedb

# EnterpriseDB database cluster superuser
pg_superuser: enterprisedb

# Home directory of postgres user
pg_user_home: "/var/lib/edb"
pg_data_dir: "/var/lib/edb/as{{ pg_major_version }}/data"
pg_bin_path: "/usr/edb/as{{ pg_major_version }}/bin"

# PostgreSQL port
pg_port: 5444

# PostgreSQL service
pg_service: edb-as-{{ pg_major_version }}

# PostgreSQL environment variables
pg_env_vars:
  - "PATH=/usr/edb/as{{ pg_major_version }}/bin:$PATH"
  - "LD_LIBRARY_PATH=/usr/edb/as{{ pg_major_version }}/lib:$LD_LIBRARY_PATH"
  - "PGLOCALEDIR=/usr/edb/as{{ pg_major_version }}/share/locale"
  - "PGDATA={{ pg_data_dir }}"

# Directory for UNIX sockets
pg_unix_socket_directories:
  - /var/run/postgresql
```

## Dependencies

None.

## Example Playbook

    - hosts: database
      become: yes
      # See: https://github.com/ansible/ansible/issues/16048#issuecomment-229012509
      vars:
        ansible_ssh_pipelining: true
      vars_files:
        - vars/main.yml
      roles:
        - dirkcaumueller.postgresql

*Inside `vars/main.yml`*:

    pg_databases:
      - name: example_db
    pg_users:
      - name: example_user
        password: supersecure

## License

MIT

## Author Information

This role was created in 2019 by Dirk C. Aumueller.
