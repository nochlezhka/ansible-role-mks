<!-- DOCSIBLE START -->

# 📃 Role overview

## ansible-role-mks



Description: your role description


| Field                | Value           |
|--------------------- |-----------------|
| Readme update        | 21/07/2024 |

### Defaults

**These are static variables with lower priority**

#### File: defaults/main.yml

| Var          | Type         | Value       |Required    | Title       |
|--------------|--------------|-------------|-------------|-------------|
| [mks_version](defaults/main.yml#L2)   | str   | `2.0.0`  |  n/a  |  n/a |
| [mks_mode](defaults/main.yml#L3)   | str   | `https`  |  n/a  |  n/a |
| [mks_domain](defaults/main.yml#L4)   | str   | `mks.homeless.ru`  |  n/a  |  n/a |
| [mks_support_email](defaults/main.yml#L5)   | str   | `bulgakova@homeless.ru`  |  n/a  |  n/a |
| [use_local_db](defaults/main.yml#L6)   | bool   | `False`  |  n/a  |  n/a |
| [set_logo](defaults/main.yml#L7)   | bool   | `False`  |  n/a  |  n/a |
| [initial_setup](defaults/main.yml#L8)   | bool   | `False`  |  n/a  |  n/a |
| [use_ext_disk](defaults/main.yml#L9)   | bool   | `True`  |  n/a  |  n/a |
| [env_vars](defaults/main.yml#L10)   | dict   | `{'TZ': 'Etc/GMT-3', 'SYMFONY_DEBUG': 1, 'TRUSTED_HOSTS': '^mks\\.homeless\\.ru$', 'APP_VER': '${MKS_VERSION}', 'NGINX_HTTPS': 'off', 'DB_NAME': 'homeless', 'MYSQL_DATABASE': 'homeless', 'ORG_NAME_SHORT': 'Название организации', 'ORG_NAME': 'СПб БОО «Название организации»', 'ORG_DESCRIPTION': 'Благотворительная общественная организация «Название организации», работающая в Санкт-Петербурге по программе помощи бездомным и малоимущим', 'ORG_DESCRIPTION_SHORT': 'СПб БОО «Название организации», работающей в Санкт-Петербурге с бездомными и малоимущими гражданами', 'ORG_CITY': 'г. Санкт-Петербург', 'ORG_CONTACTS_FULL': 'Межрегиональная благотворительная общественная организация помощи бездомным «Название организации» (СПб БОО «Название организации») ОГРН 1000000000000, ИНН 7800000000, КПП 780000000 Россия, 192000, Санкт-Петербург, Улица ул., дом 1 Соцслужба: т/ф +7(812)123-0000; офис: т/ф +7(812)123-0000', 'DISPENSARY_NAME': 'Городской наркологический диспансер', 'DISPENSARY_ADDRESS': '-укажите адрес-', 'DISPENSARY_PHONE': '-укажите телефон-', 'EMPLOYMENT_NAME': 'Агентство занятости населения', 'EMPLOYMENT_ADDRESS': '-укажите адрес-', 'EMPLOYMENT_INSPECTION': 'Государственную трудовую инспекцию в г. Санкт-Петербурге (Тел.: (812) 747-37-85 с 14.00 до 16.00; 198095, Санкт-Петербург, ул. Зои Космодемьянской, д. 28, лит. А; адрес для подачи жалоб в сети Интернет: http://онлайнинспекция.рф )', 'SANITATION_NAME': 'ГУ «Санкт-Петербургская городская дезинфекционная станция Минздрава России»', 'SANITATION_ADDRESS': 'ул. Ивашенцева, 5', 'SANITATION_TIME': '10:00-16:00'}`  |  n/a  |  n/a |





### Tasks


#### File: tasks/external_disk.yml

| Name | Module | Has Conditions |
| ---- | ------ | --------- |
| Use external disk for data | block | True |
| Create a ext4 filesystem on ext disk | community.general.filesystem | False |
| Mount ext disk to the MKS storage/uploads folder | ansible.posix.mount | False |

#### File: tasks/migrations.yml

| Name | Module | Has Conditions |
| ---- | ------ | --------- |
| Execute migrations | ansible.builtin.shell | False |
| Change admin password | ansible.builtin.shell | True |

#### File: tasks/install.yml

| Name | Module | Has Conditions |
| ---- | ------ | --------- |
| Install mks in HTTPS mode | block | True |
| Create folders for HTTPS installation | ansible.builtin.file | False |
| Run Nginx container | ansible.builtin.shell | False |
| Run certbot container | ansible.builtin.shell | False |
| Waiting for HTTPS certificate issue | ansible.builtin.pause | False |
| Launch a new version of MKS (local db) | ansible.builtin.shell | True |
| Launch a new version of MKS (external db) | ansible.builtin.shell | True |
| Install MKS in HTTP mode | block | True |
| Launch a new version of MKS (local db) | ansible.builtin.shell | True |
| Launch a new version of MKS (external db) | ansible.builtin.shell | True |
| Pause for 15 second; Wait until app became available | ansible.builtin.pause | False |

#### File: tasks/main.yml

| Name | Module | Has Conditions |
| ---- | ------ | --------- |
| Recursively remove MKS sources directory | ansible.builtin.file | False |
| Create MKS directories if they do not exist | ansible.builtin.file | False |
| Update  MKS storage/uploads folder permissions | ansible.builtin.file | False |
| Clone a github repository | git | False |
| Copy docker-compose file | ansible.builtin.copy | False |
| Copy .env file | ansible.builtin.template | False |
| Copy logo files | ansible.builtin.copy | True |
| Unnamed | ansible.builtin.include_tasks | False |
| Unnamed | ansible.builtin.include_tasks | False |
| Unnamed | ansible.builtin.include_tasks | False |







## Author Information
your name

#### License

license (GPL-2.0-or-later, MIT, etc)

#### Minimum Ansible Version

2.1

#### Platforms

No platforms specified.
<!-- DOCSIBLE END -->