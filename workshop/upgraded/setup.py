from setuptools import setup

tests_require = ['pytest']

setup(
    name = "guachi",
    version = "0.0.6",
    packages = ['guachi'],
    include_package_data=True,
    # No longer need distribute_setup.py
    author = "Alfredo Deza",
    author_email = "alfredodeza [at] gmail [dot] com",
    description = "Global, persistent configurations as dictionaries",
    long_description = """\
When projects start to grow, the need for a globally accessible configuration
manager is obvious.

Having configurations mapped to dictionaries is really useful, but can create a
problem with memory.

**Guachi** not only holds persistent dictionaries on disk, but it also maps
INI style keys to dictioanry keys, and can fill in the default values if some
of them are missing.

You do not need to know anything about how **guachi** stores the values, just
treat it like a regular dictionary!

User Interaction
------------------
Let's assume you are dealing with a Twitter application that uses a ``ini`` file.
This is a sampla INI file and how it looks::

    [DEFAULT]

    app.twitter.username = alfredodeza
    app.update.frequency = 60
    app.load.startup = False

We have a username, a frequency and a different setting for the startup option.

Lets deal with that::

    ini_file = ``/Users/alfredo/.twwiter.ini``
    conf = ConfigMapper(config_db_path)
    conf.set_config(ini_file)

That's it! At this point, **guachi** has parsed the config file and stored the values.

Lets query them calling our keys::

    >>> db_conf = conf.stored_config()
    >>> db_conf['frequency']
    60

"""
)