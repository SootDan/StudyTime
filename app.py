"""
SQlite3: Database
Datetime: Converts current time to ISO 8601 for SQL
Json: Imports strings to be used in the program; keeps code clean.
"""
from sqlite3 import Connection, Cursor, connect, Row
from datetime import date
from json import load

class StudyTime:
    """
    The app.
    """
    def __init__(self) -> None:
        self.connection: Connection = connect("studytime.sqlite")
        self.connection.row_factory = Row
        self.cursor: Cursor = self.connection.cursor()
        self.subjects: dict[str, float] = {}


    def initialize_app(self) -> None:
        """
        Initializes/creates the SQL databank and adds all subjects into a list.
        """
        subject_count: list[Cursor] = \
            self.cursor.execute("SELECT name FROM sqlite_master").fetchall()

        if len(subject_count) == 0:
            self.create_subjects()
        else:
            self.load_subjects(subject_count)


    def create_subjects(self) -> None:
        """
        Creates the study subjects and loads them into code.
        """
        print(self.output_strings("create_subjects"))
        subject_name: str = ""
        subject_time: float = 0.0

        while True:
            print(self.output_strings("exit_create_subjects"))
            subject_name: str = input("Name: ")
            if subject_name.upper() == "D":
                break
            subject_time: float = input("Time (in hours): ") * 60
            self.subjects.update({subject_name: subject_time})

        for subject_name, time_req in self.subjects.items():
            self.cursor.execute(f"CREATE TABLE {subject_name} (date DATE, time INTEGER)")
            self.cursor.execute(f"INSERT INTO {subject_name} VALUES (?, ?)", \
                (date.today(), time_req))
        self.connection.commit()


    def load_subjects(self, subjects: list[Cursor]) -> None:
        """
        Loads the subjects and stats into the code.
        """
        for subject in subjects:
            print(self.cursor.execute(f"SELECT * FROM {subject[0]}").fetchall()[0])
            #TODO: Fix method


    def output_strings(self, message: str) -> str:
        """
        Transfers the json strings to the code to stop clutter.
        """
        with open("strings.json", "r", encoding="utf-8") as json:
            return load(json).get(message)

study_time = StudyTime()
study_time.initialize_app()
