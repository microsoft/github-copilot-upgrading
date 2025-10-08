from configparser import ConfigParser
from os.path import isfile

class DictMatch(object):

    def __init__(self, config=None, mapped_options={}, mapped_defaults={}):
        self.config = config
        self.mapped_options = mapped_options
        self.mapped_defaults = mapped_defaults

    def options(self):
        # If all fails we will always have default values
        configuration = self.defaults()

        try:
            if self.config == None or isfile(self.config) == False:
                configuration = self.defaults()
                return configuration

        except TypeError:
            # if we are getting a ready-to-go dict then we still try
            # to do our little translation-and-map thing and if that
            # comes out as empty, then we assume keys are already
            # translated
            if type(self.config) is dict:
                configuration = self.key_matcher(self.config, return_empty=True)
                if not configuration:
                    configuration = self.defaults(self.config)
                return configuration

            # we could get an object that is dict-like but type(object)
            # doesn't recognize it as a dict
            else:
                configuration = self.key_matcher(self.config)
                return configuration

        else: # this will get executed *only* if we are seeing a file
            try:
                parser = ConfigParser()
                parser.read(self.config)
                file_options = parser.defaults()
                configuration = self.key_matcher(file_options)
            except Exception as error:
                raise OptionConfigurationError(error)

        return configuration


    def key_matcher(self, original, return_empty=False):
        converted_opts = {}

        for key, value in self.mapped_options.items():
            try:
                file_value = original[key]
                converted_opts[value] = file_value
            except KeyError:
                pass # we will fill any empty values later with config_defaults

        if len(converted_opts) == 0 and return_empty == True:
            return False
        try:
            configuration = self.defaults(converted_opts)
            return configuration
        except Exception as error:
            raise OptionConfigurationError(error)


    def defaults(self, config=None):
        """From the config dictionary it checks missing values and
        adds the defaul ones for them if any"""
        if config == None:
            return self.mapped_defaults

        for key in self.mapped_defaults.keys():
            try:
                config[key]
                if config[key] == '':
                    config[key] = self.mapped_defaults[key]
            except KeyError:
                config[key] = self.mapped_defaults[key]
        return config


class OptionConfigurationError(Exception):
    """Base class for exceptions in this module."""
    pass
