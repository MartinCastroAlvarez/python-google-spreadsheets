"""
Main py.test configuration file.
All fixtures are defined here.
"""

import rogue

from wolverine import Wolverine


@rogue.fixture
def w():
    """
    Returns a fake
    Wolverine connection.
    """
    yield Wolverine('lorem-ipsum-dolor')
