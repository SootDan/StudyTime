"""
SQlite3: Database
Datetime: Converts current time to ISO 8601 for SQL
"""
from sqlite3 import Connection, Cursor, connect
from datetime import date

class StudyTime:
    """
    The app.
    """
    def __init__(self) -> None:
        self.connection: Connection = connect("studytime.sqlite")
        self.cursor: Cursor = self.connection.cursor()
        self.subjects: dict = {}


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
        Creates the uni subjects and loads them into code.
        """
        print("""Looks like you haven't made a StudyTime yet.
        Select the name and time required for each subject.""")
        subject_name: str = ""
        subject_time: float = 0.0

        while True:
            print("If done, type \"D\".")
            subject_name: str = input("Name: ")
            if subject_name.upper() == "D":
                break
            subject_time: int = input("Time (in hours): ")
            self.subjects.update({subject_name: subject_time})

        for subject, time_req in self.subjects.items():
            self.cursor.execute(f"CREATE TABLE {subject} (date DATE, time INTEGER)")
            self.cursor.execute(f"INSERT INTO {subject} VALUES (?, ?)", (date.today(), time_req))
        self.connection.commit()


    def load_subjects(self, subjects: list[Cursor]):
        """
        Loads the subjects and stats into the code.
        """
        #TODO: Add functionality
        for subject in subjects:
            print(subject)

study_time = StudyTime()
study_time.initialize_app()
