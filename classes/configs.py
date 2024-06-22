'''
configs.py
'''
import click

from utils import typechecks



class Configs:
    '''
    Configs class
    '''



    def __init__(self, country_list):
        '''
        Parameters
        ----------
        country_list : list<str>
            List of countries
        '''
        typechecks.check(country_list, list)
        self.country_list = country_list



    @staticmethod
    def prompt_create():
        '''
        Prompt create the configs

        Returns
        -------
        Config
        '''
        return Configs(click.prompt('country_list', type=list, default=[
            'IT',
            'DE'
        ], show_default=True))



    def prompt_modify(self):
        '''
        Modify the configuration using click prompt
        '''
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
        return Configs(configs_dict['country_list'])



    def to_dict(self):
        '''
        Convert configs to dict

        Returns
        -------
        dict
        '''
        return {
            'country_list': self.country_list
        }
