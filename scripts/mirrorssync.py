'''
mirrorssync.py
'''
import json
import click

from utils import datetimes



_TEMPLATE_FILE = '''\
#
# File generated automatically using `mirrorssync.py`
# Do not change or modify it
# Date: {date:s}
#

{server_list:s}
'''



@click.command()
@click.argument('url-list-str', type=str)
def _main(url_list_str):
    url_list = json.loads(url_list_str)
    with open('/etc/pacman.d/mirrorlist.mirrorssync', 'w', encoding='utf-8') as file:
        file.write(_TEMPLATE_FILE.format(date=f"{datetimes.now().isoformat()}", server_list='\n'.join(f"Server = {url}" for url in url_list)))



if __name__ == '__main__':
    _main()
