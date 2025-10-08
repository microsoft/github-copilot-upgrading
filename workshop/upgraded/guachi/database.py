import sqlite3

BASE = """CREATE TABLE IF NOT EXISTS _guachi_data (key PRIMARY KEY, value)"""
OPT_MAP = """CREATE TABLE IF NOT EXISTS _guachi_options (key PRIMARY KEY, value)"""
DEF_MAP = """CREATE TABLE IF NOT EXISTS _guachi_defaults (key PRIMARY KEY, value)"""

class dbdict(dict):

    def __init__(self, path, table='_guachi_data'):
        dict.__init__(self)
        self.table = table
        self.db_filename = path
        self.con = sqlite3.connect(self.db_filename)
        self.con.execute(BASE)
        self.con.execute(OPT_MAP)
        self.con.execute(DEF_MAP)

        self.select_value = "SELECT value FROM %s WHERE key=?" % self.table
        self.select_key = "SELECT key FROM %s WHERE key=?" % self.table
        self.update_value = "UPDATE %s SET value=? WHERE key=?" % self.table
        self.insert_key_value = "INSERT INTO %s (key,value) VALUES (?,?)" % self.table
        self.delete_key = "DELETE FROM %s WHERE key=?" % self.table
        self.select_keys = "SELECT key from %s" % self.table
        self.select_all = "SELECT * from %s" % self.table

    def __getitem__(self, key):
        row = self.con.execute(self.select_value,(key,)).fetchone()
        if not row:
            raise KeyError("key '%s' not found in persistent dictionary" % key)
        return row[0]

    def __setitem__(self, key, item):
        try:
            if self.con.execute(self.select_key, (key,)).fetchone():
                self.con.execute(self.update_value, (item,key))
            else:
                self.con.execute(self.insert_key_value,(key, item))
        except sqlite3.InterfaceError as e:
            raise sqlite3.InterfaceError(e)

        self.con.commit()
        return dict.__setitem__(self, key, item)

    def __delitem__(self, key):
        if self.con.execute(self.select_key ,(key,)).fetchone():
            self.con.execute(self.delete_key ,(key,))
            self.con.commit()
        else:
             raise KeyError( "key '%s' not found in persistent dictionary" % key)

    def get(self, key, default=None):
        """Since we lazy load the dict we need to re-implement ``get``"""
        row = self.con.execute(self.select_value,(key,)).fetchone()
        if not row:
            return default
        return row[0]

    def keys(self):
        return [row[0] for row in self.con.execute(self.select_keys).fetchall()]

    def items(self):
        return [row for row in self.con.execute(self.select_all).fetchall()]

    def get_all(self):
        """If you need to get absolutely everything at once - ugh.
        This can get really expensive and defeats the purpose but oh well"""
        dict_all = {}
        for key, value in self.con.execute(self.select_all):
            dict_all[key] = value
        return dict_all

    def _integrity_check(self):
        """Make sure we are doing OK"""
        try:
            integrity = self.con.execute("pragma integrity_check").fetchone()
            if integrity == (u'ok',):
                return True
        except Exception as error:
            return error

    def _close(self):
        self.con.close()
