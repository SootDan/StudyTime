"""
Handles the table and SQL queries.
"""
from sqlite3 import Connection, Cursor, connect, PARSE_DECLTYPES    # Database
from datetime import date   # Converts current time to ISO 8601 for SQL.
from json import load   # Imports strings to be used in the program; keeps code clean.
from enum import Enum   # Eases access to SQL and further decluttering.
#from pandas import read_sql_query  # Formats SQL tables into readable strings.

class StudyTime:
    """
    The app.
    """
    def __init__(self, db: str) -> None:
        self.connection: Connection = connect(f"{db}.sqlite", detect_types=PARSE_DECLTYPES)
        self.cursor: Cursor = self.connection.cursor()
        self.sql_commands: Enum = Enum("SQLEnum", ["SUBJECTS"])
        self.subjects: list[Cursor] = self.sql_parser("SUBJECTS")


    def initialize_app(self) -> None:
        """
        Initializes/creates the SQL databank and adds all subjects into a list.
        """
        if len(self.subjects) == 0:
            self.create_subjects()
            self.initialize_app()
        else:
            self.load_subjects()

        self.app_navigator()


    def app_navigator(self) -> None:
        """
        Navigates the app and lets the user edit and manipulate data.
        """
        #TODO: Clean user input and implement method
        self.json_strings("welcome_navigation")
        db_id: int = int(input("ID: "))
        subj_current: list[Cursor] = self.sql_parser("SUBJECTS")[db_id][0]
        print(subj_current)


    def create_subjects(self) -> None:
        """
        Creates the study subjects and loads them into code.
        """
        self.json_strings("create_subjects")
        subj_name: str = ""
        subj_time: float = 0.0
        subjects: dict[str, float] = {}

        while True:
            self.json_strings("exit_create_subjects")
            subj_name: str = input("Name: ")
            if subj_name.upper() == "D":    # Done
                break
            if subj_name.upper() == "M":    # Mistake
                rm_key: dict = list(subjects)[-1]
                subjects.pop(rm_key)
            else:
                #TODO: Clean user input
                subj_time: float = float(input("Time (in hours): "))
                subjects.update({subj_name: subj_time})

        for subj_name, time_req in subjects.items():
            self.cursor.execute(f"""CREATE TABLE {subj_name}
            (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, date DATE, time FLOAT)""")
            self.cursor.execute(f"INSERT INTO {subj_name} VALUES (?, ?, ?)", \
                (None, date.today(), time_req))
        self.connection.commit()


    def load_subjects(self) -> None:
        """
        Loads the subjects and stats into the code.
        """
        i: int = 0
        for subject in self.subjects:
            subj_name: str = f"{subject[0]} (ID: {i})"
            subj_time_req: float = self.cursor.execute(f"SELECT time FROM {subject[0] \
                } WHERE id=1").fetchone()[0]
            subj_time_spent: float = self.cursor.execute(f"SELECT SUM(time) FROM {subject[0] \
                } WHERE NOT id=1").fetchone()[0]
            subj_time_spent = subj_time_spent if subj_time_spent is not None else 0.0

            print(f"SUBJECT:\t\t{subj_name}")
            print(f"HOURS REQUIRED:\t\t{subj_time_req} HOURS")
            print(f"HOURS SPENT:\t\t{subj_time_spent} HOURS")
            print(f"HOURS LEFT:\t\t{subj_time_req - subj_time_spent} HOURS")
            print("############\t\t############")
            i += 1


    def json_strings(self, message: str) -> None:
        """
        Transfers the json strings to the code to stop clutter.
        """
        with open("strings.json", "r", encoding="utf-8") as json:
            print(load(json).get(message))


    def sql_parser(self, command: Enum) -> list[Cursor]:
        """
        SQL command handler.
        """
        if command == "SUBJECTS":
            return self.cursor.execute("""SELECT name FROM sqlite_master
            WHERE NOT name=\"sqlite_sequence\"""").fetchall()
        else:
            return []


study_time = StudyTime("studytime")
study_time.initialize_app()
