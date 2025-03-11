'''
system_upgrade.py
'''
import sys
from datetime import timedelta
import json
import click

from utils import prints
from utils import commands
from utils import paths
from utils import datetimes
from utils import utils
from classes.core_configs import CoreConfigs
from classes.configs import Configs



@click.command()
@click.argument('is-modify', type=bool)
@click.argument('is-only-sync', type=bool)
@click.argument('is-only-rank', type=bool)
@click.argument('no-sync', type=bool)
@click.argument('no-rank', type=bool)
def _main(is_modify, is_only_sync, is_only_rank, no_sync, no_rank):
    '''
    Core command. Use easydup instead
    '''
    core_configs_path = paths.resolve_path(paths.folder_path(paths.resolve_link_path(__file__)), 'core-configs.json')
    print(f"core_configs_path is `{core_configs_path}`")
    configs_path = paths.resolve_path(paths.folder_path(paths.resolve_link_path(__file__)), 'configs.json')
    print(f"configs_path is `{configs_path}`")

    if not paths.is_entry(core_configs_path):
        init_datetime = datetimes.create(1970, 1, 1)
        with open(core_configs_path, 'w', encoding='utf-8') as file:
            file.write(json.dumps(CoreConfigs(init_datetime, init_datetime).to_dict(), indent=2))

    if paths.is_folder(core_configs_path):
        prints.red(f"`{core_configs_path}` is a folder")
        sys.exit(1)

    with open(core_configs_path, 'r', encoding='utf-8') as file:
        core_configs = CoreConfigs.from_dict(json.loads(file.read()))

    if not paths.is_entry(configs_path):
        with open(configs_path, 'w', encoding='utf-8') as file:
            file.write(json.dumps(Configs.prompt_create().to_dict(), indent=2))

    if paths.is_folder(configs_path):
        prints.red(f"`{configs_path}` is a folder")
        sys.exit(1)

    with open(configs_path, 'r', encoding='utf-8') as file:
        configs = Configs.from_dict(json.loads(file.read()))

    if is_modify:
        configs.prompt_modify()
        with open(configs_path, 'w', encoding='utf-8') as file:
            file.write(json.dumps(configs.to_dict(), indent=2))
        sys.exit(0)

    is_sync = (datetimes.now() - core_configs.update_datetime > timedelta(days=7)) and (not no_sync)
    is_rank = not no_rank

    if is_only_sync or is_sync:
        utils.sync_mirrors(configs)
        core_configs.update_datetime = datetimes.today()
        with open(core_configs_path, 'w', encoding='utf-8') as file:
            file.write(json.dumps(core_configs.to_dict(), indent=2))

    if is_only_sync:
        commands.run('sudo pacman -Syy', True)
        sys.exit(0)

    if is_only_rank or is_rank:
        commands.run('rankmirrors --parallel --verbose /etc/pacman.d/mirrorlist.mirrorssync | sudo tee /etc/pacman.d/mirrorlist', True)

    if is_only_rank:
        sys.exit(0)

    commands.run(f"sudo pacman -Sy{('y' if is_sync else '')}u", True)
    commands.run('yay -Sua', True)
    commands.run('sudo paccache -ruk0', True)
    commands.run('sudo paccache -rk2', True)
    commands.run('fwupdmgr refresh --force', True)
    commands.run('fwupdmgr get-updates', True)
    commands.run('fwupdmgr update', True)
    commands.run('sudo find / -iname "*pacnew*"', True)



if __name__ == '__main__':
    # pylint: disable-next=no-value-for-parameter
    _main()
