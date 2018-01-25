"""
Wolverine lets you connect
with Google Spreadsheets.
"""

import os
import json

import time
import random

import logging
import pygsheets

logger = logging.getLogger(__name__)

# pylint: disable=invalid-name


class Wolverine(object):
    """
    Google Sheets connector.
    """

    def __init__(self, sheet_id):
        """
        Constructor.
        """

        # Initializing.
        self._sheets = {}
        self._gsheet = None

        # Validate SID.
        logger.debug("Wolverine connection with %s initialized.", sheet_id)
        assert sheet_id, sheet_id
        self.sheet_id = sheet_id

    @property
    def gsheet(self):
        """
        Get Google Sheet connection.
        """

        # Check if already exists.
        if not self._gsheet:

            # Open a new connection.
            logger.debug("Loading creentials from $env...")

            # We will work in this file.
            credentials = os.path.join(os.sep,
                                       "tmp",
                                       ".w-{}-{}.json".format(random.randint(0, 100),
                                                              time.time()))

            # Dump creentials into a temporal file.
            c = {
                "private_key_id": os.environ['GOOGLE_PRIVATE_KEY_ID'],
                "private_key": os.environ['GOOGLE_PRIVATE_KEY'].replace("\\n", "\n"),
                "client_email": os.environ['GOOGLE_CLIENT_EMAIL'],
                "client_id": os.environ['GOOGLE_CLIENT_ID'],
                "type": os.environ['GOOGLE_TYPE'],
            }

            # This tmp file should not exist.
            assert not os.path.isfile(credentials), "Wolverinte temp file already exists!"

            # Save credentials into file
            logger.debug("Generating a temporal credentials file at %s", credentials)
            with open(credentials, "w") as f:
                json.dump(c, f)

            # Authroize google connection.
            # http://pygsheets.readthedocs.io/en/latest/authorizing.html
            logger.debug("Authorizing your Google credentials: %s", c)
            google_connection = pygsheets.authorize(service_file=credentials)

            # Remove temporal file.
            logger.debug("Cleaning temporal files...")
            os.remove(credentials)

            # Get sheet from google connection.
            logger.debug("Opening a new connection with Google Sheets...")
            self._gsheet = google_connection.open_by_key(self.sheet_id)

        # Return credentials.
        return self._gsheet

    def getSheet(self, sname):
        """
        Get Google Sheet by name.
        """

        # Check if sheet is already loaded.
        if sname not in self._sheets:

            # Sheet is not already loaded.
            logger.debug("Loading Google Sheet: %s", sname)
            self._sheets[sname] = self.gsheet.worksheet_by_title(sname)

        # Return Google Sheet.
        return self._sheets[sname]

    def getTotalRows(self, sname):
        """
        Returns the total amount of rows.
        """

        # Initializing.
        logger.debug("Getting total amount of rows: %s", sname)
        assert sname, "No $sname."

        # Send fake count.
        if os.environ.get('PYTEST', False):
            logger.debug("This is just test. Let's say I just have 10 rows...")
            return 10

        # Return total rows.
        x = self.getSheet(sname).rows
        logger.debug("There are %s rows.", x)
        return x

    def getTotalColumns(self, sname):
        """
        Returns the amount of columns in a sheet.
        """

        # Initializing...
        logger.debug("Getting total amount of columns: %s", sname)
        assert sname, "No $sname."

        # Send fake count.
        if os.environ.get('PYTEST', False):
            logger.debug("This is just test. Let's say I just have 10 cols...")
            return 10

        # Return total cols.
        x = self.getSheet(sname).cols
        logger.debug("There are %s cols.", x)
        return x

    def getCells(self, sname, x, y, mode="ROWS"):
        """
        Get some cells as a json matrix.
        """

        # Initializing...
        logger.debug("Getting cells from %s x=%s y=%s as %s",
                     sname,
                     x,
                     y,
                     mode)

        # Validating arguments.
        try:
            assert sname, "No $sname."
            assert x, "No $x."
            assert y, "No $y."
            assert mode, "No mode."
            assert mode in ("ROWS", "COLUMNS"), mode
            assert isinstance(x, tuple), "$x must be a tuple."
            assert isinstance(y, tuple), "$y must be a tuple."
            assert len(x) == 2, "$x must have a length of 2."
            assert len(y) == 2, "$y must have a length of 2."
            assert x[0] > 0, "$x[0] must be positive."
            assert y[0] > 0, "$y[0] must be positive."
            assert x[1] >= x[0], "$x[1] must be higher or equal to $x[0]."
            assert y[1] >= y[0], "$x[1] must be higher or equal to $x[0]."
            assert x[1] <= self.getTotalRows(sname), "x[1] is too high."
            assert y[1] <= self.getTotalRows(sname), "y[1] is too high."
        except AssertionError as e:
            raise ValueError(e)

        # Send fake values.
        if os.environ.get('PYTEST', False):
            logger.debug("This is just a test; hardcoding rows...")
            return [
                ["code", "email", "python"],
                ["1", "test1@gmail.com", "yes"],
                ["2", "test2@gmail.com", "yes"],
                ["3", "test3@gmail.com", "no"],
            ]

        # First, getting sheet.
        logger.debug("Loading google sheet...")
        sh = self.getSheet(sname)

        # Get reall cells.
        logger.debug("Getting cells...")
        sheet_cells = list(sh.get_values((x[0], y[0]),
                                         (x[1], y[1]),
                                         majdim=mode)) or []

        # Return cells as list.
        logger.debug("Found: %s", sheet_cells)
        return sheet_cells

    def iterator(self, sname, bulk=50):
        """
        Generator for the whole sheet.
        """

        # Initializing...
        logger.debug("Iterating over: %s", sname)
        assert sname, "No $sname."

        # Get Header.
        y = self.getTotalColumns(sname)
        sheet_header = self.getCells(sname, (1, 1), (1, y), mode="ROWS")[0]
        logger.debug("Head is: %s", sheet_header)

        # Control when to exsit loop.
        must_exit = False

        # Load Body.
        i = 2
        while i < self.getTotalRows(sname) and not must_exit:

            # Get a group of additional rows.
            logger.debug("Fetching more rows...")
            j = min(i + bulk, self.getTotalRows(sname))
            for row in self.getCells(sname, (i, j), (1, y), mode="ROWS"):

                # We received a group of cells.
                logger.debug("Body is: %s", row)

                # Is the body empty?
                if not row or (len(row) == 1 and not row[0]):

                    # Exit if there are no more rows to fetch.
                    logger.debug("No more rows to fetch!")
                    must_exit = True
                    break

                # Convert row to dict.
                data_dict = {}
                for k in range(0, min(len(sheet_header), len(row))):
                    if sheet_header[k]:
                        data_dict[sheet_header[k]] = row[k]

                # Return row as dict.
                logger.debug("Returning: %s", data_dict)
                yield data_dict

            # Move cursor to
            # the end of the body.
            logger.debug("Moving cursor to %s", j)
            i = j

        assert i > 2, i
