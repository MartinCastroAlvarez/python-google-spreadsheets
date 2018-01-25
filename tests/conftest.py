"""
Main py.test configuration file.
All fixtures are defined here.
"""

import pytest

from wolverine import Wolverine


@pytest.fixture
def w():
    """
    Returns a fake
    Wolverine connection.
    """
    yield Wolverine('lorem-ipsum-dolor')
