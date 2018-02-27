"""
Functional Testing, external
connections are performed.
"""

import os
import random

import rogue


@rogue.functional_test()
def test_big_data(w):
    """
    Test how long it takes to
    upload huge amounts of data.
    """
    w.sheet_id = os.environ.get('GOOGLE_SHEET_ID')
    assert w.sheet_id
    sname = "wolverine_test_big_data"
    assert sname
    w.create(sname)
    max_row = 30
    max_col = random.randint(400, 1000)
    data = []
    for _ in range(max_col):
        row = []
        for _ in range(max_row):
            row.append('A')
        data.append(row)
    w.upload(sname, data)
    row = None
    for row in w.iterator(sname, bulk=10):
        assert isinstance(row, dict)
        break
    assert row
    w.delete(sname)


@rogue.functional_test()
def test_write(w):
    """
    Functional Test to write
    a new Google Sheet.
    """
    w.sheet_id = os.environ.get('GOOGLE_SHEET_ID')
    assert w.sheet_id
    sname = "wolverine_test"
    assert sname
    w.create(sname)
    data = [
        ('a', 'b', 'c'),
        (1, 2, 3),
        (4, 5, 6),
        (7, 8, 9),
    ]
    w.upload(sname, data)
    row = None
    for row in w.iterator(sname, bulk=10):
        assert isinstance(row, dict)
        assert row['a'] == '1', row
        assert row['b'] == '2', row
        assert row['c'] == '3', row
        break
    assert row
    w.delete(sname)


@rogue.functional_test()
def test_create(w):
    """
    Functional Test for creating
    the same worksheet multiple times.
    It should NOT fail.
    """
    w.sheet_id = os.environ.get('GOOGLE_SHEET_ID')
    assert w.sheet_id
    sname = "wolverine_test_create"
    assert sname
    w.create(sname)
    w.create(sname)
    w.delete(sname)


@rogue.functional_test()
def test_delete(w):
    """
    Functional Test for deleting
    the same worksheet multiple times.
    It should NOT fail.
    """
    w.sheet_id = os.environ.get('GOOGLE_SHEET_ID')
    assert w.sheet_id
    sname = "wolverine_test_delete"
    assert sname
    w.create(sname)
    w.delete(sname)
    w.delete(sname)


@rogue.functional_test()
def test_read(w):
    """
    Functional Test to read
    an existing Google Sheet.
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
