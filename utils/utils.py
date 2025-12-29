'''
utils.py
'''
import sys
from datetime import datetime
from datetime import timedelta
import re
import json

from utils import colors
from utils import prints
from utils import paths
from utils import commands
from utils import requestss



_TEMPLATE_LOG_MIRROR = '''\
{url:s}
    last_check: {last_check}
    active: {active}
    last_sync: {last_sync} ({delta})\
'''

_TEMPLATE_LOG_INFO = '''\
Total mirrors: {totals:d}
    inactive or unsynched: {errors:s}
    not recently synched: {warnings:s}
    missing infos: {no_infos:s}\
'''



def _retrieve_arch_mirrors(configs):
    '''
    Download and check mirror status
    
    Parameters
    ----------
    configs : Configs
        configs
    '''
    mirror_url_list = []
    error_country_list = []
    for country in configs.country_list:
        try:
            response = requestss.get(f"https://archlinux.org/mirrorlist/?country={country}&protocol=https&ip_version=4&ip_version=6&use_mirror_status=on")
            mirror_url_list += [server_str.split(' = ')[1] for server_str in response.text.split('\n') if 'Server = ' in server_str]
        except Exception:
            error_country_list.append(country)

    if not mirror_url_list:
        prints.red(' ✗ No mirror url list')
        sys.exit(1)
    if error_country_list:
        prints.yellow(' ✗ Missing mirrors for some countries')
        for error_country in error_country_list:
            prints.yellow(f'   {error_country}')

    response = requestss.get('https://archlinux.org/mirrors/status/json')
    response_dict = response.json()
    last_check_datetime = datetime.fromisoformat(response_dict['last_check'])

    error_mirror_dict_list = []
    warning_mirror_dict_list = []
    ok_mirror_url_list = []
    no_info_mirror_url_list = []
    for url in mirror_url_list:
        is_match = False
        for mirror_dict in response_dict['urls']:
            if re.search(f"^{mirror_dict['url']}", url):
                is_match = True
                if not mirror_dict['active'] or not mirror_dict['last_sync']:
                    error_mirror_dict_list.append(mirror_dict)
                    break
                if last_check_datetime - datetime.fromisoformat(mirror_dict['last_sync']) > timedelta(days=1):
                    warning_mirror_dict_list.append(mirror_dict)
                    break
                ok_mirror_url_list.append(url)
                break
        if is_match:
            continue
        no_info_mirror_url_list.append(url)

    for mirror_dict in error_mirror_dict_list:
        prints.red(_TEMPLATE_LOG_MIRROR.format(url=mirror_dict['url'], last_check=last_check_datetime, active=mirror_dict['active'], last_sync=mirror_dict['last_sync'], delta=last_check_datetime - datetime.fromisoformat(mirror_dict['last_sync'])))
    for mirror_dict in warning_mirror_dict_list:
        prints.yellow(_TEMPLATE_LOG_MIRROR.format(url=mirror_dict['url'], last_check=last_check_datetime, active=mirror_dict['active'], last_sync=mirror_dict['last_sync'], delta=last_check_datetime - datetime.fromisoformat(mirror_dict['last_sync'])))
    for url in no_info_mirror_url_list:
        prints.yellow(_TEMPLATE_LOG_MIRROR.format(url=url, last_check=last_check_datetime, active='unknown', last_sync='unknown', delta=''))
    print(_TEMPLATE_LOG_INFO.format(totals=len(mirror_url_list), errors=colors.red(len(error_mirror_dict_list)), warnings=colors.yellow(len(warning_mirror_dict_list)), no_infos=colors.yellow(len(no_info_mirror_url_list))))
    if error_mirror_dict_list:
        prints.red(' ✗ Some mirrors unactive or unsynched')
    if warning_mirror_dict_list:
        prints.yellow(' ✗ Some mirrors not recently synched')
    if no_info_mirror_url_list:
        prints.yellow(' ✗ Missing infos for some mirrors')
    if not ok_mirror_url_list:
        ok_mirror_url_list = no_info_mirror_url_list
        prints.yellow(' ✗ Missing reliable mirrors, switched to missing info mirrors')
    if not ok_mirror_url_list:
        prints.red(' ✗ No usable mirrors')
        sys.exit(1)
    if not error_mirror_dict_list and not warning_mirror_dict_list and not no_info_mirror_url_list:
        prints.green(' ✓ Good mirror status')

    return ok_mirror_url_list



def _retrieve_arch_arm_mirrors():
    '''
    Returns the list of mirrors to use
    '''
    with open('/etc/pacman.d/mirrorlist', 'r', encoding='utf-8') as file:
        mirror_url_list = re.findall(r'\#?\ *Server\ *\=\ *([^\ ]*)\n', file.read())

    return mirror_url_list



def sync_mirrors(configs):
    '''
    Saves the mirrors using the ad hoc script
    
    Parameters
    ----------
    configs : Configs
        configs
    '''
    mirror_url_list = []
    match configs.operative_system:
        case 'arch':
            mirror_url_list = _retrieve_arch_mirrors(configs)
        case 'arch_arm':
            mirror_url_list = _retrieve_arch_arm_mirrors()
        case 'arch_32':
            raise Exception('arch_32 not supported')

    print(f"Used mirrors: {len(mirror_url_list)}")

    commands.run(f"sudo PYTHONPATH={paths.resolve_path(paths.get_folder_path(__file__), '..')} python {paths.resolve_path(paths.get_folder_path(__file__), '../scripts/mirrors_sync.py')} '{json.dumps(mirror_url_list)}'", True)
