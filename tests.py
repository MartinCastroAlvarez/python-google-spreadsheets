from wolverine import Wolverine
import pytest


@pytest.fixture
def sid():
    yield "1s3kY46A0KBPnM3_HEMcu8CvquSsCPUV-pxCaknv2GQ4"


@pytest.fixture
def sname():
    yield "Opportunities"


@pytest.fixture
def w(sid):
    yield Wolverine(sid)


class TestWolverine(object):

    def test_get_total_rows(self, w, sname):
        total = w.getTotalRows(sname)
        assert type(total) is int
        assert total > 0

    def test_get_total_columns(self, w, sname):
        total = w.getTotalColumns(sname)
        assert type(total) is int
        assert total > 0

    def test_get_a_few_cells(self, w, sname):
        cells = w.getCells(sname, (1, 3), (2, 5))
        a = cells[0][0]
        b = cells[0][1]
        cells = w.getCells(sname, (1, 3), (1, 5))
        assert cells[0][1] == a
        assert cells[0][2] == b

    def test_iterator(self, w, sname):
        i = 0
        for row in w.iterator(sname):
            i += 1
            assert type(row) is dict
            assert "Code" in row
        assert i > 0
