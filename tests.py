from wolverine import Wolverine
import pytest
import os


@pytest.fixture
def sid():
    yield "1s3kY46A0KBPnM3_HEMcu8CvquSsCPUV-pxCaknv2GQ4"


@pytest.fixture
def sname():
    yield "Opportunities"


@pytest.fixture
def w(sid):

    # Open a new connection.
    w = Wolverine(sid)

    # Mock gsheet.
    class mock_gsheet(object):
        def __init__(self):
            self.rows = 1
            self.cells = 1
        def worksheet_by_title(self, sname):
            class G(object):
                def __init__(self):
                    self.rows = 30
                    self.cols = 20
                def get_values(self, *args, **kwargs):
                    yield ["Code", "Email", "Test"]
                    yield [4, 5, 6]
                    yield [7, 8, 9]
                def iterator(self, *args, **kwargs):
                    yield {"Code": "1"}
                    yield {"Code": "1"}
                    yield {"Code": "1"}
            return G()
    w.__class__.gsheet = mock_gsheet()

    # Return fake connection.
    yield w


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

    def test_iterator(self, w, sname):
        i = 0
        for row in w.iterator(sname):
            i += 1
            assert type(row) is dict, row
            assert "Code" in row, row
        assert i > 0
