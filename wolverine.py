"""
Wolverine lets you connect with Google Spreadsheets.

Example:
>>> config_path = os.path.join(os.sep, "home", os.getlogin(), ".wolverine")
>>> c = Configuration(config_path)
>>> credentials = c.get_credentials("ampush")
>>> c = Google(credentials)
>>> s = c.get_spreadsheet("1t90q05AOBAiO2k5jegM0F4WSO8kMvaPzQsSSsF3HtPw")
>>> w = s.get_worksheet("Sheet6")
>>> w.get_cells(1, 1)
>>> try:
...     w = s.get_worksheet("Sheet10")
...     except Worksheet.NotFound:
...     w = s.create_worksheet("Sheet12")
...     w.clear_cells()
...     w.update_cells(1, 1, [["a"]])
>>>     w.upload_csv("/opt/ampush/payments/tmp/dataloss/results.csv")
... finally:
...     s.delete_worksheet("Sheet12")
"""

import os
import csv
import json
import uuid

import begin

import googleapiclient
import pygsheets


class Credentials(object):
    """
    Authentication credentials.

    Example:
    {
        "type": "service_account",
        "project_id": "198239819823981298312",
        "private_key_id": "19823981823981298398123",
        "private_key": "-----BEGIN PRIVATE KEY-----\n...",
        "client_email": "ampushexperimenter@appspot.gserviceaccount.com",
        "client_id": "",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/..."
    }
    """

    GOOGLE_PRIVATE_KEY_ID = "private_key_id"
    GOOGLE_PRIVATE_KEY = "private_key"
    GOOGLE_CLIENT_EMAIL = "client_email"
    GOOGLE_CLIENT_ID = "client_id"
    GOOGLE_TYPE = "type"
    GOOGLE_TOKEN_URI = "token_uri"
    GOOGLE_DEFAULT_TOKEN_URI = "https://oauth2.googleapis.com/token"

    def __init__(self, credentials: dict=None):
        """
        Constructing credentials.

        @raises ValueError: If credentials are empty.
        @raises TypeError: If credentials are not a valid dict.
        """
        if not credentials:
            raise ValueError("credentials")
        if not isinstance(credentials, dict):
            raise TypeError("credentials")
        self.__data = credentials

    def __str__(self) -> str:
        """ String serializer. """
        return "<Credentials: {}>".format(self.to_json())

    @property
    def private_key_id(self) -> str:
        """
        Access Google private key ID.

        @raises KeyError: If key name is not in JSON credentials.
        @raises ValueError: If key name is empty.
        @raises TypeError: if key value is not a valid string.
        @raises AttributeError: If credentials data is empty.

        @returns: Key value as a string.
        """
        if not self.__data:
            raise AttributeError("credentials")
        if self.GOOGLE_PRIVATE_KEY_ID not in self.__data:
            raise KeyError(self.GOOGLE_PRIVATE_KEY_ID)
        if not self.__data[self.GOOGLE_PRIVATE_KEY_ID]:
            raise ValueError(self.GOOGLE_PRIVATE_KEY_ID)
        if not isinstance(self.__data[self.GOOGLE_PRIVATE_KEY_ID], str):
            raise TypeError(self.GOOGLE_PRIVATE_KEY_ID)
        return self.__data[self.GOOGLE_PRIVATE_KEY_ID]

    @property
    def private_key(self) -> str:
        """
        Access Google private key.

        @raises KeyError: If key name is not in JSON credentials.
        @raises ValueError: If key name is empty.
        @raises TypeError: if key value is not a valid string.
        @raises AttributeError: If credentials data is empty.

        @returns: Key value as a string.
        """
        if not self.__data:
            raise AttributeError("credentials")
        if self.GOOGLE_PRIVATE_KEY not in self.__data:
            raise KeyError(self.GOOGLE_PRIVATE_KEY)
        if not self.__data[self.GOOGLE_PRIVATE_KEY]:
            raise ValueError(self.GOOGLE_PRIVATE_KEY)
        if not isinstance(self.__data[self.GOOGLE_PRIVATE_KEY], str):
            raise TypeError(self.GOOGLE_PRIVATE_KEY)
        return self.__data[self.GOOGLE_PRIVATE_KEY]

    @property
    def client_id(self) -> str:
        """
        Access Google client ID.

        @raises KeyError: If key name is not in JSON credentials.
        @raises TypeError: if key value is not a valid string.
        @raises AttributeError: If credentials data is empty.

        @returns: Key value as a string.
        """
        if not self.__data:
            raise AttributeError("credentials")
        if self.GOOGLE_CLIENT_ID not in self.__data:
            raise KeyError(self.GOOGLE_CLIENT_ID)
        if not isinstance(self.__data[self.GOOGLE_CLIENT_ID], str):
            raise TypeError(self.GOOGLE_CLIENT_ID)
        return self.__data[self.GOOGLE_CLIENT_ID]

    @property
    def client_email(self) -> str:
        """
        Access Google client email.

        @raises KeyError: If key name is not in JSON credentials.
        @raises ValueError: If key name is empty.
        @raises TypeError: if key value is not a valid string.
        @raises AttributeError: If credentials data is empty.

        @returns: Key value as a string.
        """
        if not self.__data:
            raise AttributeError("credentials")
        if self.GOOGLE_CLIENT_EMAIL not in self.__data:
            raise KeyError(self.GOOGLE_CLIENT_EMAIL)
        if not self.__data[self.GOOGLE_CLIENT_EMAIL]:
            raise ValueError(self.GOOGLE_CLIENT_EMAIL)
        if not isinstance(self.__data[self.GOOGLE_CLIENT_EMAIL], str):
            raise TypeError(self.GOOGLE_CLIENT_EMAIL)
        return self.__data[self.GOOGLE_CLIENT_EMAIL]

    @property
    def account_type(self) -> str:
        """
        Access Google account type.

        @raises KeyError: If key name is not in JSON credentials.
        @raises ValueError: If key name is empty.
        @raises TypeError: if key value is not a valid string.
        @raises AttributeError: If credentials data is empty.

        @returns: Key value as a string.
        """
        if not self.__data:
            raise AttributeError("credentials")
        if self.GOOGLE_TYPE not in self.__data:
            raise KeyError(self.GOOGLE_TYPE)
        if not self.__data[self.GOOGLE_TYPE]:
            raise ValueError(self.GOOGLE_TYPE)
        if not isinstance(self.__data[self.GOOGLE_TYPE], str):
            raise TypeError(self.GOOGLE_TYPE)
        return self.__data[self.GOOGLE_TYPE]

    def to_json(self) -> dict:
        """ JSON serializer. """
        return {
            self.GOOGLE_PRIVATE_KEY_ID: self.private_key_id,
            self.GOOGLE_PRIVATE_KEY: self.private_key,
            self.GOOGLE_CLIENT_EMAIL: self.client_email,
            self.GOOGLE_CLIENT_ID: self.client_id,
            self.GOOGLE_TYPE: self.account_type,
            self.GOOGLE_TOKEN_URI: self.GOOGLE_DEFAULT_TOKEN_URI,
        }


class Configuration(object):
    """ Configuration file entity. """

    def __init__(self, config_path: str=None):
        """
        Constructing Profile file.

        @param config_path: Configuration file name.

        @raises ValueError: If path name is empty.
        @raises TypeError: if path name is not a valid string.
        @raises RuntimeError: If config file is not a valid file.
        """
        if not config_path:
            raise ValueError("config_path")
        if not isinstance(config_path, str):
            raise TypeError("config_path")
        if not os.path.isfile(config_path):
            raise RuntimeError("File not found:", config_path)
        self.__config_path = config_path 

    def __str__(self) -> str:
        """ String serializer. """
        return "<Configuration: {}>".format(self.__config_path)

    def get_credentials(self, profile_name: str=None) -> object:
        """
        Public method to access profile credentials.

        @param profile_name: Profile name.

        @raises ValueError: If name is empty.
        @raises TypeError: If name is an invalid string.
        @raises RuntimeError: If config path is not a valid file.
        @raises KeyError: If name is not found in the profiles file.
        @raises ValueError: If file is not a valid JSON file.

        @returns: Credentials instance.
        """
        if not profile_name:
            raise ValueError("profile_name")
        if not isinstance(profile_name, str):
            raise TypeError("profile_name")
        if not os.path.isfile(self.__config_path):
            raise RuntimeError("File not found:", self.__config_path)
        with open(self.__config_path, "r") as file_buffer:
            data = json.loads(file_buffer.read().strip())
        if not data:
            raise RuntimeError(self.__config_path)
        if not isinstance(data, dict):
            raise RuntimeError(type(data))
        if profile_name not in data:
            raise KeyError(profile_name)
        if not data[profile_name]:
            raise RuntimeError("profile_name")
        return Credentials(data[profile_name])


class Google(object):
    """ Google Drive connection. """

    def __init__(self, credentials: Credentials=None):
        """
        Constructing Google connection.

        @param: Google credentials.

        @raises TypeError: If credentials are not valid.
        @raises ValueError: If credentials are empty.
        """
        if not credentials:
            raise ValueError("credentials")
        if not isinstance(credentials, Credentials):
            raise TypeError(type(credentials))
        self.__credentials = credentials
        self.__connection = None

    def __str__(self) -> str:
        """ String serializer. """
        return "<Google: {}>".format(self.__connection)

    @property
    def connection(self) -> object:
        """
        This methods connects with Google server.

        @raises AttributeError: If credentials are empty.

        @returns: Google connection instance.
        """
        if not self.__connection:
            if not self.__credentials:
                raise AttributeError("credentials")
            random_name = "w-{}.json".format(uuid.uuid4().hex)
            temp_file = os.path.join(os.sep, "tmp", random_name)
            with open(temp_file, "w") as file_buffer:
                json.dump(self.__credentials.to_json(), file_buffer)
            self.__connection = pygsheets.authorize(service_file=temp_file)
            os.remove(temp_file)
        return self.__connection

    def get_spreadsheet(self, spreadsheet_id: str=None) -> object:
        """
        Constructing spreadsheet.

        @param spreadsheet_id: Spreadsheet ID.

        @raises ValueError: If spreadsheet ID is empty.
        @raises TypeError: If spreadsheet ID is an invalid string.

        @returns: Spreadsheet instance.
        """
        if not spreadsheet_id:
            raise ValueError("spreadsheet_id")
        if not isinstance(spreadsheet_id, str):
            raise TypeError("spreadsheet_id")
        s = self.connection.open_by_key(spreadsheet_id)
        return Spreadsheet(s)


class Spreadsheet(object):
    """ Google Spreadsheet. """

    def __init__(self, spreadsheet: pygsheets.spreadsheet.Spreadsheet=None):
        """
        Constructing spreadsheet.

        @param spreadsheet: Spreadsheet object.

        @raises ValueError: If spreadsheet is empty.
        @raises TypeError: If spreadsheet is invalid.
        """
        if not spreadsheet:
            raise ValueError("spreadsheet")
        if not isinstance(spreadsheet, pygsheets.spreadsheet.Spreadsheet):
            raise TypeError("spreadsheet")
        self.__spreadsheet = spreadsheet

    @property
    def spreadsheet(self):
        """ Property to access raw spreadsheet. """
        return self.__spreadsheet

    def __str__(self) -> str:
        """ String serializer. """
        return "<Spreadsheet: {}>".format(self.__spreadsheet)

    def get_worksheet(self, sheet_name: str=None) -> object:
        """
        Returns work sheet name.

        @param sheet_name: Sheet name.

        @raises ValueError: If sheet is empty.
        @raises TypeError: If sheet is an invalid string.

        @returns: Worksheet instance.
        """
        if not sheet_name:
            raise ValueError("sheet_name")
        if not isinstance(sheet_name, str):
            raise TypeError("sheet_name")
        try:
            w = self.__spreadsheet.worksheet_by_title(sheet_name)
        except pygsheets.exceptions.WorksheetNotFound:
            raise Worksheet.NotFound(sheet_name)
        return Worksheet(w)

    def delete_worksheet(self, sheet_name: str=None) -> None:
        """
        Delete work sheet by name.

        @param sheet_name: Sheet name.

        @raises ValueError: If sheet is empty.
        @raises TypeError: If sheet is an invalid string.

        @returns: None.
        """
        if not sheet_name:
            raise ValueError("sheet_name")
        if not isinstance(sheet_name, str):
            raise TypeError("sheet_name")
        try:
            self.__spreadsheet.del_worksheet(self.get_worksheet(sheet_name).worksheet)
        except Worksheet.NotFound:
            pass

    def create_worksheet(self, sheet_name: str=None) -> object:
        """
        Creates a work sheet by name.

        @param sheet_name: Sheet name.

        @raises ValueError: If sheet is empty.
        @raises TypeError: If sheet is an invalid string.

        @returns: Worksheet instance.
        """
        if not sheet_name:
            raise ValueError("sheet_name")
        if not isinstance(sheet_name, str):
            raise TypeError("sheet_name")
        try:
            w = self.__spreadsheet.add_worksheet(sheet_name)
            return Worksheet(w)
        except googleapiclient.errors.HttpError as e:
            if "already exists" in str(e):
                return self.get_worksheet(sheet_name)
            raise


class Worksheet(object):
    """ Google Worksheet. """

    class NotFound(Exception):
        """ Raised when Worksheet was not found. """

    class AlreadyExists(Exception):
        """ Raised when Worksheet already exists. """

    def __init__(self, worksheet: pygsheets.spreadsheet.Worksheet=None):
        """
        Constructing sheet.

        @param worksheet: Spreadsheet object.

        @raises ValueError: If sheet is empty.
        @raises TypeError: If sheet is invalid.
        """
        if not worksheet:
            raise ValueError("sheet")
        if not isinstance(worksheet, pygsheets.spreadsheet.Worksheet):
            raise TypeError("sheet")
        self.__worksheet = worksheet

    @property
    def worksheet(self):
        """ Property to access raw worksheet. """
        return self.__worksheet

    def __str__(self) -> str:
        """ String serializer. """
        return "<Worksheet: {} [{} x {}]>".format(self.__worksheet, self.height, self.width)

    @property
    def height(self) -> int:
        """ Returns sheet number of rows. """
        return self.__worksheet.rows

    @property
    def width(self) -> int:
        """ Returns sheet number of columns. """
        return self.__worksheet.cols

    def clear_cells(self) -> None:
        """ Clear all cells. """
        self.__worksheet.clear(start="A1", end=None)

    def get_cells(self, x1: int=None, y1: int=None, x2: int=None, y2: int=None) -> list:
        """
        Returns a worksheet cell.

        @param x1: Coordinates.
        @param x2: Coordinates.
        @param y1: Coordinates.
        @param y2: Coordinates.

        @raises TypeError: If coordinate is not a valid integer.
        @raises ValueError: If range is invalid.

        @returns: List of lists.
        """
        if not isinstance(x1, int):
            raise TypeError("x1")
        if not isinstance(y1, int):
            raise TypeError("y1")
        if not x2:
            x2 = x1
        if not y2:
            y2 = y1
        if not isinstance(x2, int):
            raise TypeError("x2")
        if not isinstance(y2, int):
            raise TypeError("y2")
        if x1 < 1:
            raise ValueError("x1")
        if y1 < 1:
            raise ValueError("x1")
        if x2 < 1:
            raise ValueError("x2")
        if y2 < 1:
            raise ValueError("y2")
        if x1 > x2:
            raise ValueError(x1, x2)
        if y1 > y2:
            raise ValueError(y1, y2)
        return self.__worksheet.get_values((x1, y1), (x2, y2), include_tailing_empty=False) or []

    def update_cells(self, x: int=None, y: int=None, data: object=None) -> None:
        """
        Update cells.

        @param x: Coordinates.
        @param y: Coordinates.
        @param data: Data to update.

        @raises TypeError: If coordinates are not valid integers.
        @raises TypeError: If data matrix is not valid.
        @raises ValueError: If range is invalid.

        @returns: None.
        """
        if not isinstance(x, int):
            raise TypeError("x")
        if not isinstance(y, int):
            raise TypeError("y")
        if x < 1:
            raise ValueError("x")
        if y < 1:
            raise ValueError("x")
        if not isinstance(data, list):
            raise TypeError("data")
        self.__worksheet.update_values((x, y), data)

    def upload_csv(self, file_path: str=None) -> None:
        """
        Upload worksheet from local file.

        @param file_path: Local file path.

        @raises ValueError: If file path is empty.
        @raises TypeError: If file path is not a valid string.
        @raises RuntimeError: If file doesn't exist.

        @returns: None.
        """
        if not isinstance(file_path, str):
            raise TypeError("file_path")
        if not os.path.isfile(file_path):
            raise RuntimeError("File not found:", file_path)
        with open(file_path, "r") as file_buffer:
            reader = csv.reader(file_buffer)
            data = list(reader)
        self.update_cells(1, 1, data)

    def rows(self):
        """ Iterates over all rows. """
        page_size = 200
        row = 1
        while row <= self.height:
            cells = self.get_cells(row, 1, row + page_size, self.width)
            yield from cells
            row += page_size


class Default(object):
    """ Default variables. """
    PROFILE = "ampush"
    CONFIG = os.path.join(os.sep, "home", os.getlogin(), ".wolverine")


@begin.subcommand
@begin.logging
def details(profile=Default.PROFILE,
            config_path=Default.CONFIG,
            spreadsheet_id=None,
            worksheet_name=None):
    """
    Print Spreadsheet content.

    @param profile: Profile name.
    @param config_path: Configuration path.
    @param spreadsheet_id: Spreadsheet ID.
    @param worksheet_name: Worksheet name.
    """
    c = Configuration(config_path)
    c = c.get_credentials(profile)
    g = Google(c)
    s = g.get_spreadsheet(spreadsheet_id)
    w = s.get_worksheet(worksheet_name)
    for row in w.rows():
        print(row)
        

@begin.subcommand
@begin.logging
def upload(profile=Default.PROFILE,
           config_path=Default.CONFIG,
           spreadsheet_id=None,
           worksheet_name=None,
           file_path=None):
    """
    Upload CSV to Google Spreadsheets.

    @param profile: Profile name.
    @param config_path: Configuration path.
    @param file_path: CSV file path.
    @param spreadsheet_id: Spreadsheet ID.
    @param worksheet_name: Worksheet name.
    """
    c = Configuration(config_path)
    c = c.get_credentials(profile)
    g = Google(c)
    s = g.get_spreadsheet(spreadsheet_id)
    try:
        w = s.get_worksheet(worksheet_name)
    except Worksheet.NotFound:
        w = s.create_worksheet(worksheet_name)
    finally:
        w.clear_cells()
        w.upload_csv(file_path)


@begin.start(lexical_order=True, short_args=True)
@begin.logging
def run():
    """
    Main task.
    This method will be called by executing this script from the CLI.
    """
