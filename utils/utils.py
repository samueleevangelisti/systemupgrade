'''
utils.py
'''
import sys
from datetime import datetime
from datetime import timedelta
import re
import json
import requests

from utils import colors
from utils import prints
from utils import paths
from utils import commands



_TEMPLATE_LOG_MIRROR = '''\
{url:s}
    last_check: {last_check}
    active: {active}
    last_sync: {last_sync} {delta}\
'''

_TEMPLATE_LOG_INFO = '''\
Total mirrors: {total:s}
    inactive or unsynched: {error:s}
    not recently synched: {warning:s}
    missing infos: {no_info:s}\
'''



def sync_mirrors(system_upgrade_configs):
    url_list = []
    for country in system_upgrade_configs.country_list:
        response = requests.get(f"https://archlinux.org/mirrorlist/?country={country}&protocol=https&ip_version=4&ip_version=6&use_mirror_status=on", timeout=60)
        url_list += [server_str.split(' = ')[1] for server_str in response.text.split('\n') if 'Server = ' in server_str]
    response = requests.get('https://archlinux.org/mirrors/status/json', timeout=60)
    response_dict = response.json()
    last_check_date_time = datetime.fromisoformat(response_dict['last_check'])
    mirror_dict_list_error = []
    mirror_dict_list_warning = []
    mirror_url_list = []
    url_list_no_info = []
    for url in url_list:
        is_match = False
        for mirror_dict in response_dict['urls']:
            if re.match(f"^{mirror_dict['url']}", url):
                is_match = True
                if not mirror_dict['active'] or not mirror_dict['last_sync']:
                    mirror_dict_list_error.append(mirror_dict)
                elif last_check_date_time - datetime.fromisoformat(mirror_dict['last_sync']) > timedelta(days=1):
                    mirror_dict_list_warning.append(mirror_dict)
                else:
                    mirror_url_list.append(url)
        if not is_match:
            url_list_no_info.append(url)
    for mirror_dict in mirror_dict_list_error:
        prints.red(_TEMPLATE_LOG_MIRROR.format(url=mirror_dict['url'], last_check=last_check_date_time, active=mirror_dict['active'], last_sync=mirror_dict['last_sync'], delta=last_check_date_time - datetime.fromisoformat(mirror_dict['last_sync'])))
    for mirror_dict in mirror_dict_list_warning:
        prints.yellow(_TEMPLATE_LOG_MIRROR.format(url=mirror_dict['url'], last_check=last_check_date_time, active=mirror_dict['active'], last_sync=mirror_dict['last_sync'], delta=last_check_date_time - datetime.fromisoformat(mirror_dict['last_sync'])))
    for url in url_list_no_info:
        prints.yellow(_TEMPLATE_LOG_MIRROR.format(url=url, last_check=last_check_date_time, active='unknown', last_sync='unknown', delta=''))
    print(_TEMPLATE_LOG_INFO.format(total=colors.green(len(url_list)), error=colors.red(len(mirror_dict_list_error)), warning=colors.yellow(len(mirror_dict_list_warning)), no_info=colors.yellow(len(url_list_no_info))))
    if mirror_dict_list_error:
        prints.red(' ✗ Some mirrors unactive or unsynched')
    if mirror_dict_list_warning:
        prints.yellow(' ✗ Some mirrors not recently synched')
    if url_list_no_info:
        prints.yellow(' ✗ Missing infos for some mirrors')
    if not mirror_dict_list_error and not mirror_dict_list_warning and not url_list_no_info:
        prints.green(' ✓ Good mirror status')
    mirror_url_list = mirror_url_list or url_list_no_info
    if not mirror_url_list:
        prints.red(' ✗ No usable mirrors')
        sys.exit(1)
    print(f"Used mirrors: {colors.green(len(mirror_url_list))}")
    commands.run(f"sudo PYTHONPATH={paths.resolve_path(paths.folder_path(__file__), '..')} python {paths.resolve_path(paths.folder_path(__file__), '../scripts/mirrorssync.py')} '{json.dumps(mirror_url_list)}'", True)



def rank_mirrors():
    pass
