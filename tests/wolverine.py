"""
Unit Testing. No external
connections are performed.
"""

import os
import pytest


@pytest.mark.skipif(not os.environ.get('PYTEST'),
                    reason='Unit Tests not executed in QA mode.')
class TestDownload(object):
    """
    Test get data
    from spreadsheet.
    """

    def test_get_total_rows(self, w):
        """
        Get total rows from spreadsheet.
        """
        total = w.getTotalRows('lorem')
        assert isinstance(total, int)
        assert total > 0

    def test_get_total_columns(self, w):
        """
        Get total columns from spreadsheet.
        """
        total = w.getTotalColumns('lorem')
        assert isinstance(total, int)
        assert total > 0

    def test_get_a_few_cells(self, w):
        """
        Load a few cells from the spreadsheet.
        """
        cells = w.getCells('lorem', (1, 3), (2, 5))
        assert cells[0][0]
        assert cells[0][1]

    def test_iterator(self, w):
        """
        Iterate over all spreadsheet rows.
        """
        i = 0
        for row in w.iterator('lorem'):
            i += 1
            assert dict(row), row
            assert "code" in row, row
            assert "email" in row, row
        assert i > 0
