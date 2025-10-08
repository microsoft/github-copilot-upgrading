
import os
import unittest
from guachi import ConfigMapper
from guachi.database import dbdict

# An example of a default config dict
DEFAULT_CONFIG = {
            'frequency': 60,
            'master': 'False',
            'host': 'localhost',
            'ssh_user': 'root',
            'ssh_port': 22,
            'hosts_path': '/opt/pacha',
            'hg_autocorrect': 'True',
            'log_enable': 'False',
            'log_path': 'False',
            'log_level': 'DEBUG',
            'log_format': '%(asctime)s %(levelname)s %(name)s %(message)s',
            'log_datefmt' : '%H:%M:%S'
            }


class test_ConfigMapper(unittest.TestCase):

    def setUp(self):
        try:
            os.remove('/tmp/guachi.db')
            os.remove('/tmp/foo_guachi.db')
        except Exception:
            pass 

    def tearDown(self):
        try:
            os.remove('/tmp/guachi.db')
            os.remove('/tmp/foo_guachi.db')
        except Exception:
            pass 


    def test_init(self):
        foo = ConfigMapper('/tmp')
        expected = '/tmp/guachi.db'
        actual = foo.path 
        self.assertEqual(actual, expected) 


    def test__call__(self):
        """ConfigMapper should be callable"""
        foo = ConfigMapper('/tmp')
        actual = foo()
        expected = {}
        self.assertEqual(actual, expected) 


    def test_set_ini_options(self):
        foo = ConfigMapper('/tmp')
        my_config = {'config.db.port':'db_port'}
        foo.set_ini_options(my_config)
        db = dbdict(path='/tmp/guachi.db', table='_guachi_options')
        expected = my_config
        actual = db.get_all()
        self.assertEqual(actual, expected) 


    def test_set_default_options(self):
        foo = ConfigMapper('/tmp')
        my_config = {'db_port':1234}
        foo.set_default_options(my_config)
        db = dbdict(path='/tmp/guachi.db', table='_guachi_defaults')
        expected = my_config
        actual = db.get_all()
        self.assertEqual(actual, expected) 


    def test_get_ini_options(self):
        foo = ConfigMapper('/tmp')
        my_config = {'config.db.port':'db_port'}
        foo.set_ini_options(my_config)
        defaults = foo.get_ini_options()
        actual = defaults['config.db.port']
        expected = 'db_port'
        self.assertEqual(actual, expected) 


    def test_get_default_options(self):
        foo = ConfigMapper('/tmp')
        my_config = {'db_port':1234}
        foo.set_default_options(my_config)
        defaults = foo.get_default_options()
        actual = defaults['db_port']
        expected = 1234
        self.assertEqual(actual, expected) 


    def test_path_verify_file(self):
        foo = ConfigMapper('/tmp/foo_guachi.db')
        actual = foo._path_verify('/tmp/foo_guachi.db')
        expected = '/tmp/foo_guachi.db'
        self.assertEqual(actual, expected) 


    def test_path_verify_dir(self):
        foo = ConfigMapper('/tmp')
        actual = foo._path_verify('/tmp')
        expected = '/tmp/guachi.db'
        self.assertEqual(actual, expected) 

    def test_update_config_dict_empty(self):
        """Pass an empty dict and get defaults back"""
        foo = ConfigMapper('/tmp')
        foo.update_config({})
        db = dbdict('/tmp/guachi.db')
        actual = db.get_all()
        expected ={}
        self.assertEqual(actual, expected) 
        

    def test_update_config_dict(self):
        foo = ConfigMapper('/tmp')
        foo.update_config(DEFAULT_CONFIG)
        db = dbdict('/tmp/guachi.db')
        actual = db.get_all()
        expected = DEFAULT_CONFIG
        self.assertEqual(actual, expected) 
 
        
    def test_set_config_dict_empty(self):
        """Pass an empty dict and get defaults back"""
        foo = ConfigMapper('/tmp')
        foo.set_config({})
        db = dbdict('/tmp/guachi.db')
        actual = db.get_all()
        expected ={}
        self.assertEqual(actual, expected) 
        

    def test_set_config_dict(self):
        foo = ConfigMapper('/tmp')
        foo.set_config(DEFAULT_CONFIG)
        db = dbdict('/tmp/guachi.db')
        actual = db.get_all()
        expected = DEFAULT_CONFIG
        self.assertEqual(actual, expected) 
 

    def test_get_dict_config(self):
        foo = ConfigMapper('/tmp')
        foo.set_config(DEFAULT_CONFIG)
        actual = foo.get_dict_config()
        expected = DEFAULT_CONFIG
        self.assertEqual(actual, expected) 


    def test_integrity_check(self):
        foo = ConfigMapper('/tmp')
        foo.set_config(DEFAULT_CONFIG)
        actual = foo.integrity_check()
        self.assertTrue(actual) 


    def test_stored(self):
        foo = ConfigMapper('/tmp')
        bar = foo.stored_config()
        self.assertEqual(bar, {})


    def test_stored_get_data(self):
        """Verify we can actually get data by using stored"""
        foo = ConfigMapper('/tmp')
        bar = foo.stored_config()
        bar['a'] = 1
        self.assertEqual(bar, {'a':1})


