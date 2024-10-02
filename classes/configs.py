'''
configs.py
'''
import click
from click import Choice

from utils import typechecks



_OPERATIVE_SYSTEM_CHOICE = Choice((
    'arch',
    'arch_arm',
    'arch_32',
))
_OPERATIVE_SYSTEM_DEFAULT = 'arch'
_COUNTRY_LIST_DEFAULT = [
    'IT',
    'DE'
]



class Configs:
    '''
    Configs class
    '''



    def __init__(self, operative_system, country_list):
        '''
        Parameters
        ----------
        operative_system : str
            Operative system
        country_list : list of str
            List of countries
        '''
        typechecks.check(operative_system, str)
        typechecks.check(country_list, list)
        self.operative_system = operative_system
        self.country_list = country_list



    @staticmethod
    def prompt_create():
        '''
        Prompt create the configs

        Returns
        -------
        Config
        '''
        return Configs(click.prompt('operative_system', type=_OPERATIVE_SYSTEM_CHOICE, show_choices=True, default=_OPERATIVE_SYSTEM_DEFAULT, show_default=True), click.prompt('country_list', type=list, default=_COUNTRY_LIST_DEFAULT, show_default=True))



    def prompt_modify(self):
        '''
        Modify the configuration using click prompt
        '''
        self.operative_system = click.prompt('operative_system', type=_OPERATIVE_SYSTEM_CHOICE, show_choices=True, default=self.operative_system, show_default=True)
        self.country_list = click.prompt('country_list', type=list, default=self.country_list, show_default=True)



    @staticmethod
    def from_dict(configs_dict):
        '''
        Create configs from dict

        Parameters
        ----------
        configs_dict : dict
            dict from configs

        Returns
        -------
        Configs
        '''
        return Configs(configs_dict['operative_system'], configs_dict['country_list'])



    def to_dict(self):
        '''
        Convert configs to dict

        Returns
        -------
        dict
        '''
        return {
            'operative_system': self.operative_system,
            'country_list': self.country_list
        }
