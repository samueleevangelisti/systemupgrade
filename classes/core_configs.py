'''
core_configs.py
'''
from datetime import datetime

from utils import typechecks



class CoreConfigs:
    '''
    Core configs class
    '''



    def __init__(self, sync_datetime, update_datetime):
        '''
        Parameters
        ----------
        sync_datetime : datetime
            Last sync from repo
        update_datetime : datetime
            Last mirrors update
        '''
        typechecks.check(sync_datetime, datetime)
        typechecks.check(update_datetime, datetime)
        self.sync_datetime = sync_datetime
        self.update_datetime = update_datetime



    @staticmethod
    def from_dict(core_configs_dict):
        '''
        Create core configs from dict

        Parameters
        ----------
        core_configs_dict : dict
            dict from core configs

        Returns
        -------
        CoreConfigs
        '''
        return CoreConfigs(datetime.fromisoformat(core_configs_dict['sync_datetime']), datetime.fromisoformat(core_configs_dict['update_datetime']))



    def to_dict(self):
        '''
        Convert core configs to dict
        
        Returns
        -------
        dict
        '''
        return {
            'sync_datetime': self.sync_datetime.isoformat(),
            'update_datetime': self.update_datetime.isoformat()
        }
