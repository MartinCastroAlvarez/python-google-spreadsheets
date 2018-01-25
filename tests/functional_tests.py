"""
Functional Testing, external
connections are performed.
"""

import os
import pytest


@pytest.mark.skipif(bool(os.environ.get('PYTEST')),
                    reason='Functional Tests not executed in debug mode.')
def test_functional_test(w):
    """
    Test Functional Test.
    """

    # We inject the sheet id.
    w.sheet_id = os.environ['GOOGLE_SHEET_ID']
    assert w.sheet_id

    # We get the sheet name
    # from the local config.
    sname = os.environ['GOOGLE_SHEET_NAME']
    assert sname

    # We get the total rows
    # from this sheet.
    assert w.getTotalRows(sname) > 1

    # We get the total cols
    # from this sheet.
    assert w.getTotalColumns(sname) > 1

    # We check there is at
    # least one row.
    has_rows = False

    # We iterate over all cells.
    for row in w.iterator(sname, bulk=10):

        # This row must be
        # a Dict.
        assert isinstance(row, dict)

        # We check there is at
        # least one row.
        has_rows = True

        # We only want one row.
        break

    # We check there is at
    # least one row.
    assert has_rows
