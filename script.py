"""
The script which is used both by the CLI and GUI version of the app.
"""
from datetime import date   # Converts current time to ISO 8601 for SQL.
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
    CREATE_TABLE = Creates a table with ID, today's date, and required time. 
        Also stores metadata about the subjects.
    SELECT_SUBJECTS = Selects all subjects in a table.
    SELECT_SUBJECTS_REQ_TIME = Selects the required time 
    SELECT_SUBJECTS_DEADLINE = Selects deadline of one subject
    SELECT_SUBJECTS_DONE_TIME = Selects already studied time (0.0 if none)
    INSERT_SUBJECTS_REQ_TIME = Inserts required time for a subject
    """
    NONE = -1
    CREATE_TABLE = 0
    SELECT_SUBJECTS = 1
    SELECT_SUBJECTS_REQ_TIME = 2
    SELECT_SUBJECTS_DONE_TIME = 3
    SELECT_SUBJECTS_DEADLINE = 4
    INSERT_SUBJECTS_REQ_TIME = 5


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
        self.subjects: list[Cursor] = self.sql_handler(SQLEnum.SELECT_SUBJECTS)


    def sql_handler(self, command: SQLEnum, arg: list = None) -> list[Cursor]:
        """
        SQL command handler. See SQLEnum for further information.
        """
        match command:
            case SQLEnum.CREATE_TABLE:
                self.cursor.execute(
                    f"""CREATE TABLE {arg}(
                    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, date DATE, time DATE)""")
                self.cursor.execute(
                    f"""CREATE TABLE IF NOT EXISTS Meta(
                    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, subject {arg},
                    time_req FLOAT, deadline DATE)""")

            case SQLEnum.SELECT_SUBJECTS:
                return self.cursor.execute(
                    """SELECT name FROM sqlite_master
            WHERE name NOT IN (\"sqlite_sequence\", \"Meta\")""").fetchall()
            case SQLEnum.SELECT_SUBJECTS_REQ_TIME:
                return self.cursor.execute(
                    f"SELECT time_req FROM Meta WHERE subject=\"{arg}\"").fetchone()[0]
            case SQLEnum.SELECT_SUBJECTS_DONE_TIME:
                return self.cursor.execute(
                    f"SELECT SUM(time) FROM {arg} WHERE NOT id=1").fetchone()[0]

            case SQLEnum.SELECT_SUBJECTS_DEADLINE:
                return self.cursor.execute(
                    f"SELECT deadline FROM Meta WHERE subject=\"{arg}\"").fetchone()[0]

            case SQLEnum.INSERT_SUBJECTS_REQ_TIME:
                self.cursor.execute(
                    "INSERT INTO Meta VALUES (?, ?, ?, ?)", (None, arg[0], arg[1], date.today()))
            case _:
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
