import base64
from pathlib import Path
import unittest

import yaml
from ansible.parsing.dataloader import DataLoader
from ansible.template import Templar


ROOT = Path(__file__).resolve().parents[1]


def load_yaml(path):
    return yaml.safe_load((ROOT / path).read_text())


class InstallTests(unittest.TestCase):
    def setUp(self):
        self.variables = {
            **load_yaml('defaults/main.yml'),
            **load_yaml('vars/main.yml'),
            'secret_env_vars': {},
            'mks_version': 'release/caddy',
        }
        self.tasks = load_yaml('tasks/install.yml')
        self.launch = next(task for task in self.tasks if 'ansible.builtin.command' in task)

    def render(self, value):
        return Templar(loader=DataLoader(), variables=self.variables).template(value)

    def test_launch_modes_and_database_profiles(self):
        for mode in ('http', 'https'):
            for local_db in (False, True, 'false', 'true'):
                with self.subTest(mode=mode, local_db=local_db):
                    self.variables.update(mks_mode=mode, use_local_db=local_db)
                    argv = self.render(self.launch['ansible.builtin.command']['argv'])
                    profile = ['--profile', 'local'] if local_db in (True, 'true') else []
                    self.assertEqual(argv, ['docker-compose'] + profile + [
                        'up', '-d', '--no-build', '--remove-orphans',
                    ])
                    environment = self.render(self.launch['environment'])
                    self.assertEqual(environment['CADDY_MODE'], mode)
                    self.assertEqual(environment['MKS_VERSION'], 'release-caddy')
                    self.assertEqual(str(environment['HTTP_PORT']), '80')
                    self.assertEqual(str(environment['HTTPS_PORT']), '443')
                    rendered = self.render((ROOT / 'templates/env.j2').read_text())
                    for key, value in environment.items():
                        self.assertEqual(rendered.splitlines().count(f'{key}={value}'), 1)

    def test_custom_ports_and_reserved_environment(self):
        self.variables['env_vars'].update(HTTP_PORT=8080, HTTPS_PORT=8443, CADDY_MODE='http')
        self.variables['secret_env_vars'] = {'CADDY_MODE': 'http', 'DB_PASSWORD': 'secret'}
        environment = self.render(self.launch['environment'])
        self.assertEqual(str(environment['HTTP_PORT']), '8080')
        self.assertEqual(str(environment['HTTPS_PORT']), '8443')
        rendered = self.render((ROOT / 'templates/env.j2').read_text())
        self.assertEqual(rendered.count('CADDY_MODE='), 1)
        self.assertIn('CADDY_MODE=https', rendered)
        self.assertIn("DB_PASSWORD='secret'", rendered)

    def test_caddy_storage_permissions(self):
        storage = next(task['ansible.builtin.file'] for task in self.tasks if 'ansible.builtin.file' in task)
        self.assertEqual(storage['path'], '/opt/homeless/mks/deploy/storage/data/caddy')
        self.assertEqual(storage['owner'], '1000')
        self.assertEqual(storage['group'], '1000')
        self.assertEqual(storage['mode'], '0755')

    def test_mode_validation(self):
        conditions = self.tasks[0]['ansible.builtin.assert']['that']
        for mode, domain, email, valid in (
            ('http', '', '', True),
            ('https', 'mks.example.org', 'admin@example.org', True),
            ('https_init', 'mks.example.org', 'admin@example.org', False),
            ('https', '', 'admin@example.org', False),
            ('https', 'mks.example.org', '', False),
        ):
            with self.subTest(mode=mode, domain=domain, email=email):
                self.variables.update(mks_mode=mode, mks_domain=domain, mks_support_email=email)
                self.assertEqual(all(self.render('{{ ' + condition + ' }}') for condition in conditions), valid)

    def test_compose_compatibility_before_copy(self):
        tasks = load_yaml('tasks/main.yml')
        guard = next(task for task in tasks if 'ansible.builtin.assert' in task)
        copy = next(task for task in tasks if task.get('name') == 'Copy docker-compose file')
        self.assertLess(tasks.index(guard), tasks.index(copy))
        for service, valid in (('caddy', True), ('nginx', False)):
            with self.subTest(service=service):
                content = yaml.safe_dump({'services': {service: {}}}).encode()
                self.variables['mks_compose_source'] = {'content': base64.b64encode(content).decode()}
                condition = guard['ansible.builtin.assert']['that'][0]
                self.assertEqual(self.render('{{ ' + condition + ' }}'), valid)


if __name__ == '__main__':
    unittest.main()