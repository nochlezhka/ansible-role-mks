Role Name
=========

A brief description of the role goes here.

Requirements
# ansible-role-mks

Deploys [MKS](https://github.com/nochlezhka/mks) with Caddy, PHP and an optional
local MySQL database. Caddy obtains and renews HTTPS certificates automatically.

## Requirements

- Docker and `docker-compose` with profile support on the target host.
- Git, the `ubuntu` user, and privileges to manage Docker, files and mounts.
- The `community.general` and `ansible.posix` collections when `use_ext_disk` is enabled.
- An application Git ref and published image containing the Caddy changes from
  [MKS PR #156](https://github.com/nochlezhka/mks/pull/156).
- For HTTPS, public DNS pointing at the host and reachable TCP ports 80 and 443.

PR #156 is not merged yet. Explicitly set `mks_version` to a published image version
with Caddy; the legacy default `2.0.0` is not suitable. Set `mks_repo_branch` when
the Git ref differs from the image version. The role rejects Compose files without
the `caddy` service before replacing the installed Compose file.

## Variables

| Variable | Purpose |
| --- | --- |
| `mks_version` | Application Git ref and image tag; `/` becomes `-` in the image tag. Must contain Caddy. |
| `mks_repo_branch` | Optional override of the application Git ref. Must match the selected image's deployment configuration. |
| `mks_mode` | `https` (default) or `http`. |
| `mks_domain` | Public domain for HTTPS. |
| `mks_support_email` | ACME contact email for HTTPS. |
| `use_local_db` | Enable the Compose `local` profile (default: `false`). |
| `env_vars` | Application settings; `HTTP_PORT` and `HTTPS_PORT` override host ports 80 and 443. |
| `secret_env_vars` | Required mapping of application secrets, such as database credentials. Store in Ansible Vault. |
| `use_ext_disk` | Mount `/dev/vdb` for uploads (default: `true`). Disable when no dedicated disk is available. |
| `initial_setup` | Change the admin password using `mks_admin_password` (default: `false`). |
| `set_logo` | Copy custom logos from the playbook's `files` directory (default: `false`). |

Compose settings are saved in `/opt/homeless/mks/deploy/.env` and supplied to the
launch command. Configure mode, domain, email and version through role variables,
not duplicate entries in `env_vars` or `secret_env_vars`. If overriding `env_vars`,
include the application settings required by your deployment.

## Example

Replace the version and Git ref placeholders with matching Caddy-enabled artifacts.

```yaml
- hosts: mks
  become: true
  roles:
    - role: ansible-role-mks
      mks_version: '<published-version-with-caddy>'
      mks_repo_branch: '<git-ref-with-caddy>'
      mks_mode: https
      mks_domain: mks.example.org
      mks_support_email: admin@example.org
      use_local_db: false
      use_ext_disk: false
      secret_env_vars: '{{ vault_mks_env_vars }}'
```

## Migrating From nginx And certbot

The role uses `up -d --no-build --remove-orphans` to remove the old nginx and
certbot containers belonging to the same Compose project and start Caddy. Keep
the existing deployment directory and Compose project name when upgrading.
Containers from a different project require manual review and removal.

Certificates are stored in `storage/data/caddy`, owned by UID/GID `1000:1000`.
Back up and preserve this directory across deployments. Caddy issues new
certificates; old `storage/data/letsencrypt` and `storage/data/certbot` directories
are left untouched. Expect a brief interruption during the switch and initial
certificate issuance. Certificate availability is not checked by the role.

There is no `https_init` mode or `certbot` profile anymore. After deployment,
inspect certificate issuance with `docker logs caddy`. For manual Compose
commands, add `--profile local` when using the local database.

## Tests

Install `ansible-core>=2.16,<2.19`, then run:

```sh
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

These tests validate Ansible templating, launch modes, port overrides, storage
permissions and the legacy Compose guard without Docker or a target host.

## License

BSD
