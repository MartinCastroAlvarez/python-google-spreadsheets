from setuptools import setup
from os.path import exists
from os.path import join
from os import walk

packages = [d for d,_,__ in walk('wolverine') if exists(join(d,'__init__.py'))]

setup(
    version='2.11',
    name='wolverine',
    description='Wolverine.',
    maintainer='martin castro',
    maintainer_email='martin.castro@valleyworks.com',
    url='https://github.com/valleyworks/wolverine.git',
    packages=packages,
    include_package_data=True,
    install_requires=[
        'requests',
        'google-api-python-client',
        'pygsheets',
    ]
)

