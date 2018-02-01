"""
Functional Testing, external
connections are performed.
"""

import os
import rogue


@rogue.functional_test()
def test_functional_test(w):
    """
    Test Functional Test.
    """

    w.sheet_id = os.environ.get('GOOGLE_SHEET_ID')
    assert w.sheet_id

    sname = os.environ.get('GOOGLE_SHEET_NAME')
    assert sname

    assert w.getTotalRows(sname) > 1
    assert w.getTotalColumns(sname) > 1

    row = None
    for row in w.iterator(sname, bulk=10):
        assert isinstance(row, dict)
        break
    assert row
