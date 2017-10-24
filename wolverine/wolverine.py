import pygsheets
import logging
import os

logger = logging.getLogger(__name__)


class Wolverine(object):

    def __init__(self, sid):
        assert sid
        self.sid = sid

    @property
    def gsheet(self):
        if not hasattr(self, "_xls"):
            root = os.path.dirname(__file__)
            cpath = os.path.join(root, "credentials.json")
            gc = pygsheets.authorize(service_file=cpath)
            self._xls = gc.open_by_key(self.sid)
        return self._xls

    def getSheet(self, sname):
        if not hasattr(self, "_sheets"):
            self._sheets = {}
        if sname not in self._sheets:
            self._sheets[sname] = self.gsheet.worksheet_by_title(sname)
        return self._sheets[sname]

    def getTotalRows(self, sname):
        logger.warning("Getting total amount of rows: {}".format(sname))
        assert sname
        return self.getSheet(sname).rows

    def getTotalColumns(self, sname):
        logger.warning("Getting total amount of columns: {}".format(sname))
        assert sname
        return self.getSheet(sname).cols

    def getCells(self, sname, x, y, mode="ROWS"):
        logger.warning("Getting cells: {}".format(sname))
        assert sname
        assert mode in "ROWS", "COLUMNS"
        assert type(x) is tuple
        assert type(y) is tuple
        assert len(x) is 2
        assert len(y) is 2
        assert x[0] > 0
        assert x[1] >= x[0]
        assert x[1] <= self.getTotalRows(sname)
        assert y[0] > 0
        assert y[1] >= y[0]
        assert y[1] <= self.getTotalColumns(sname)
        sh = self.getSheet(sname)
        return list(sh.get_values((x[0], y[0]),
                                  (x[1], y[1]),
                                  majdim=mode)) or []

    def iterator(self, sname):

        # Initializing...
        logger.warning("Iterating over: {}".format(sname))
        assert sname
        head = {}

        # Get Header.
        y = self.getTotalColumns(sname)
        head = self.getCells(sname, (1, 1), (1, y), mode="ROWS")[0]

        # Load Body.
        i = 1
        while i < self.getTotalRows(sname):

            # Get a group of rows.
            j = min(i + 30, self.getTotalRows(sname))
            for body in self.getCells(sname, (i, j), (1, y), mode="ROWS")[0]:

                # The body is empty?
                if not body:
                    break

                # Return row.
                yield {head[k]: body[k] for k in range(0, min(len(head), len(body))) if head[k]}

            i = j

        assert i > 2
