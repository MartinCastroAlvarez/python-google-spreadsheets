import pygsheets
import logging
import json
import os

logger = logging.getLogger(__name__)


class Wolverine(object):

    def __init__(self, sid):
        assert sid
        self.sid = sid

    @property
    def gsheet(self):
        if not hasattr(self, "_xls"):
            logger.debug("Loading creentials from $env")
            credentials = os.path.join(os.sep, "tmp", ".wolvierne.json")
            c = {
                "private_key_id": os.environ['GOOGLE_PRIVATE_KEY_ID'],
                "private_key": os.environ['GOOGLE_PRIVATE_KEY'],
                "client_email": os.environ['GOOGLE_CLIENT_EMAIL'],
                "client_id": os.environ['GOOGLE_CLIENT_ID'],
                "type": os.environ['GOOGLE_TYPE'],
            }
            if os.path.isfile(credentials):
                os.remove(credentials)
            with open(credentials, "w") as f:
                json.dump(c, f)
            gc = pygsheets.authorize(service_file=credentials)
            os.remove(credentials)
            self._xls = gc.open_by_key(self.sid)
        return self._xls

    def getSheet(self, sname):
        if not hasattr(self, "_sheets"):
            self._sheets = {}
        if sname not in self._sheets:
            self._sheets[sname] = self.gsheet.worksheet_by_title(sname)
        return self._sheets[sname]

    def getTotalRows(self, sname):
        logger.debug("Getting total amount of rows: {}".format(sname))
        assert sname
        return self.getSheet(sname).rows

    def getTotalColumns(self, sname):
        logger.debug("Getting total amount of columns: {}".format(sname))
        assert sname
        return self.getSheet(sname).cols

    def getCells(self, sname, x, y, mode="ROWS"):
        logger.debug("Getting cells: {}".format(sname))
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

    def iterator(self, sname, bulk=50):

        # Initializing...
        logger.debug("Iterating over: {}".format(sname))
        assert sname
        head = {}

        # Get Header.
        y = self.getTotalColumns(sname)
        head = self.getCells(sname, (1, 1), (1, y), mode="ROWS")[0]
        logger.debug("Head is: {}".format(head))

        # Load Body.
        i = 2
        mustExit = False
        while i < self.getTotalRows(sname) and not mustExit:

            # Get a group of rows.
            logger.debug("Fetching more rows...")
            j = min(i + bulk, self.getTotalRows(sname))
            for body in self.getCells(sname, (i, j), (1, y), mode="ROWS"):

                # The body is empty?
                logger.debug("Body is: {}".format(body))
                if not body or (len(body) == 1 and not body[0]):
                    logger.debug("No more rows to fetch!")
                    mustExit = True
                    break

                # Return row.
                yield {head[k]: body[k] for k in range(0, min(len(head), len(body))) if head[k]}

            i = j

        assert i > 2
