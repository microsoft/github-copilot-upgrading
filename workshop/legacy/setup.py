from setuptools import setup

tests_require = ['pytest']

setup(
    name = "guachi",
    version = "0.0.6",
    packages = ['guachi'],
    include_package_data=True,
    # No longer need distribute_setup.py

    # metadata
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

Great, we now are making sure we have our data. We can actually get that value from anywhere
in our twitter app by calling it this way::

    db = ConfigMapper(config_db_path)
    conf = db.stored_config()

    frequency = conf['frequency']


Getting Deafults
---------------------
Above we inspected an INI file with some changed values. But what happens when the user
has none?

Since we set our defaults, we can be sure they are right there in case our app needs
it in some sub-module::

    >>> db = ConfigMapper(config_db_path)
    >>> conf = db.stored_config()
    >>> conf['load']
    True

Updating Values
-----------------
What if a user makes changes? We can always save and update what we read from the INI
file at load time, to make sure we have the latest changes from the user::

    conf = ConfigMapper(config_db_path)
    conf.update_config(ini_file)

Documentation
=============
Our full Documentation is hosted here. Go take a look for the full API.

http://guachi.googlecode.com/hg/docs/build/html/index.html
""",
   classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Build Tools',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
      ],

    license = "MIT",
    keywords = "configuration management persistent dictionaries dictionary parse map mapping",
    url = "http://code.google.com/p/guachi",

)

