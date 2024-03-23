'''
systemupgradeconfigs.py
'''
from datetime import datetime
from datetime import timezone
import click

from utils import typechecks



class SystemUpgradeConfigs:
    '''
    pass
    '''



    def __init__(self, update_datetime, country_list):
        typechecks.check(update_datetime, datetime)
        typechecks.check(country_list, list)
        self.update_datetime = update_datetime
        self.country_list = country_list



    @staticmethod
    def prompt_create():
        '''
        pass
        '''
        return SystemUpgradeConfigs(datetime(1970, 1, 1, tzinfo=timezone.utc), click.prompt('country_list', type=list, default=[
            'IT',
            'DE'
        ], show_default=True))



    @staticmethod
    def from_dict(configs_dict):
        '''
        pass
        '''
        return SystemUpgradeConfigs(datetime.fromisoformat(configs_dict['update_datetime']), configs_dict['country_list'])



    def to_dict(self):
        '''
        pass
        '''
        return {
            'update_datetime': self.update_datetime.isoformat(),
            'country_list': self.country_list
        }
