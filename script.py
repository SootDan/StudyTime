"""
The script which is used both by the CLI and GUI version of the app.
"""
from enum import Enum   # Eases access to SQL and further decluttering.
from glob import glob   # Finds SQLite files
from sqlite3 import Connection, Cursor, connect, PARSE_DECLTYPES    # Database
from pandas import read_json    # Imports strings to be used in the program; keeps code clean.

class Settings(Enum):
    """
    These are the settings that can be changed.
    LANGUAGE = German deDE / English enUS
    """
    NONE = -1
    LANGUAGE = 0


class SQLEnum(Enum):
    """
    SQL commands to be executed.
    SUBJECTS = Selects all subjects in a table.
    """
    NONE = -1
    SUBJECTS = 0


class App:
    """
    The class which is used both by the CLI and GUI version of the app.
    Does not execute any code of its own.
    """
    def __init__(self) -> None:
        self.files: list[str] = glob("*.sqlite")
        self.connection: Connection
        self.cursor: Cursor
        self.language = self.json_handler("language", True)
        self.subjects: list[Cursor]


    def connect_to_db(self, db_name: str) -> None:
        """
        Loads selected SQL file.
        """
        self.connection = connect(f"{db_name}.sqlite", detect_types=PARSE_DECLTYPES)
        self.cursor: Cursor = self.connection.cursor()
        self.subjects: list[Cursor] = self.sql_handler(SQLEnum.SUBJECTS)


    def sql_handler(self, command: SQLEnum) -> list[Cursor]:
        """
        SQL command handler.
        """
        if command == SQLEnum.SUBJECTS:
            return self.cursor.execute("""SELECT name FROM sqlite_master
            WHERE NOT name=\"sqlite_sequence\"""").fetchall()
        return []


    def json_handler(self, str_input: str, is_setting: bool = False,
    setting: Settings = Settings.NONE) -> str:
        """
        Transfers the json strings to the code to stop clutter. 
        Takes from the given language or setting.
        """
        mode: str = "settings" if is_setting else self.language

        if is_setting and setting is not Settings.NONE:
            lang_df = read_json("strings.json")
            settings_list = lang_df["settings"].iloc[0]
            settings_list["language"] = "enUS"
            lang_df.to_json("strings.json")

            str_output = str_input
            return str_output
        return read_json("strings.json")[mode].iloc[0][str_input]
