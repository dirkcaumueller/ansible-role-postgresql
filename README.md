# Ansible Role: PostgreSQL

[![Build Status](https://travis-ci.org/dirkcaumueller/postgresql.svg?branch=master)](https://travis-ci.org/dirkcaumueller/postgresql)

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
# Set major version of PostgreSQL
pg_major_version: 12

# PostgreSQL Development Group YUM repository url
pg_repo_url: "https://download.postgresql.org/pub/repos/yum/reporpms/EL-7-x86_64/pgdg-redhat-repo-latest.noarch.rpm"

# Set a repository to use for PostgreSQL installation
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
pg_user_password: postgres
pg_group: postgres

# PostgreSQL database cluster superuser
pg_superuser: postgres
pg_superuser_password: postgres

# Home directory of postgres user
pg_user_home: "/var/lib/pgsql"

# Set the cluster directory
pg_data_dir: "/var/lib/pgsql/{{ pg_major_version }}/data"

# Binary path
pg_bin_path: "/usr/pgsql-{{ pg_major_version }}/bin"

# Log directory
pg_log_dir: "/var/log/pgsql-{{ pg_major_version }}"

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
pg_initdb_params: "--encoding=UTF8 --wal-segsize 64 --locale=de_DE.UTF-8 --lc-collate=C --lc-ctype=C
 --data-checksums --auth-host=scram-sha-256 --auth-local=peer"

# Host based authentication (hba) entries to be added to the pg_hba.conf. This
# variable's defaults reflect the defaults that come with a fresh installation.
pg_hba_entries:
  - {type: local, database: all, user: all, auth_method: peer}
  - {type: host, database: all, user: all, address: '127.0.0.1/32', auth_method: md5}
  - {type: host, database: all, user: all, address: '::1/128', auth_method: md5}
  - {type: local, database: replication, user: all, auth_method: peer}
  - {type: host, database: replication, user: all, address: '127.0.0.1/32', auth_method: md5}
  - {type: host, database: replication, user: all, address: '::1/128', auth_method: md5}

# Global configuration options that will be set via ALTER SYSTEM in postgresql.auto.conf
pg_postgresql_conf_params: []
#  - name:
#    value:

# Add databases to cluster
pg_databases: []
# - name: exampledb # required; the rest are optional
#   lc_collate: # defaults to 'de_DE.UTF-8'
#   lc_ctype: # defaults to 'de_DE.UTF-8'
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
# - name: jdoe #required; the rest are optional
#   password: # defaults to not set
#   encrypted: # defaults to not set
#   priv: # defaults to not set
#   role_attr_flags: # defaults to not set
#   db: # defaults to not set
#   login_host: # defaults to 'localhost'
#   login_password: # defaults to not set
#   login_user: # defaults to '{{ pg_user }}'
#   login_unix_socket: # defaults to 1st of '{{ pg_unix_socket_directories }}'
#   port: # defaults to not set
#   state: # defaults to 'present'
```

## Dependencies

None.

## Example Playbook

    - hosts: database
      become: yes
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
