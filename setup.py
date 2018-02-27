"""
You can import this library
as a pip dependency.
"""

from os import walk
from os.path import exists
from os.path import join
from setuptools import setup

packages = [d for d, _, __ in walk('wolverine') if exists(join(d, '__init__.py'))]

setup(

    # This is the library
    # latest version.
    version='3.3',

    # These variabls describe
    # your package.
    name='wolverine',
    description='Wolverine.',
    maintainer='martin castro',
    maintainer_email='martin.castro@valleyworks.com',
    url='https://github.com/valleyworks/wolverine.git',

    # These are all the files
    # that will be installed
    # when you install this
    # library as a dependency.
    packages=packages,

    # This tells pip not
    # to install git version
    # data when cloning
    # the repo.
    include_package_data=False,

    # These are all the pip
    # dependencies required
    # by this library.
    install_requires=[
        'requests',
        'google-api-python-client',
        'pygsheets',
    ]

)
