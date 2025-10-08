from guachi.database import dbdict
from guachi.config import DictMatch
import os

class ConfigMapper(object):

    def __init__(self, path):
        self.path = self._path_verify(path)


    def __call__(self):
        db = dbdict(self.path)
        return db


    def set_ini_options(self, dictionary):
        """Maps your INI configuration keys to dictionary keys"""
        db = dbdict(self.path, table='_guachi_options') 
        for key, value in dictionary.items():
            db[key] = value 


    def set_default_options(self, dictionary):
        """Maps the default values that we can fill in if keys are empty"""
        db = dbdict(self.path, table='_guachi_defaults') 
        for key, value in dictionary.items():
            db[key] = value


    def get_ini_options(self):
        """Returns the dictionary that maps INI style options to 
        dictionary options"""
        db = dbdict(self.path, table='_guachi_options') 
        return db


    def get_default_options(self):
        """Returns the default options we hold"""
        db = dbdict(self.path, table='_guachi_defaults') 
        return db


    def set_config(self, configuration=None):
        """Accepts a dictionary or a file to set persistent configurations"""
        mapped_ini = self.get_ini_options()
        mapped_defaults = self.get_default_options()

        # First make sure that whatever we get, gets translated
        # into a dictionary 
        dict_match = DictMatch(configuration, mapped_ini, mapped_defaults)
        dict_config = dict_match.options()
        if len(dict_config.items()) > 0:
            db = dbdict(self.path)
            for key, value in dict_config.items():
                db[key] = value


    def update_config(self, configuration=None):
        """An alias to set_config for readability sake"""
        return self.set_config(configuration)


    def get_dict_config(self):
        """Returns the full stored configuration values as a dictionary"""
        db = dbdict(self.path)
        return db.get_all()


    def stored_config(self):
        """Access the DB directly for pay-as-you-go configuration needs
        You get an empty dict but with access to any keys when requested
        """
        db = dbdict(self.path)
        return db


    def integrity_check(self):
        """Verify the database is OK"""
        db = dbdict(self.path)
        return db._integrity_check()


    def _path_verify(self, path):
        """The need to have valid absolute paths"""
        if not os.path.isdir(path):
            return os.path.abspath(path)
        if os.path.isdir(path):
            abspath = os.path.abspath(path)
            return abspath+'/guachi.db'

