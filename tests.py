from wolverine import Wolverine
import pytest
import os


@pytest.fixture
def w():
    os.environ['PYTEST'] = 'yes'
    yield Wolverine('lorem-ipsum-dolor')


class TestWolverine(object):

    def test_get_total_rows(self, w):
        total = w.getTotalRows('lorem')
        assert type(total) is int
        assert total > 0

    def test_get_total_columns(self, w):
        total = w.getTotalColumns('lorem')
        assert type(total) is int
        assert total > 0

    def test_get_a_few_cells(self, w):
        cells = w.getCells('lorem', (1, 3), (2, 5))
        a = cells[0][0]
        b = cells[0][1]

    def test_iterator(self, w):
        i = 0
        for row in w.iterator('lorem'):
            i += 1
            assert type(row) is dict, row
            assert "code" in row, row
            assert "email" in row, row
        assert i > 0
