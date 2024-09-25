"""
CLI version of the app.
"""
from datetime import date   # Converts current time to ISO 8601 for SQL.
from script import App, Settings, SQLEnum


class StudyTime(App):
    """
    The app.
    """
    def __init__(self) -> None:
        super().__init__()

        # Initializes/creates SQL file. User can select which one they want to use and name it.
        if self.language == "default":
            print(self.json_handler("select_language"))
            select = input()
            self.language = self.json_handler(select, True, Settings.LANGUAGE)

        if len(self.files) == 0:
            print(self.json_handler("first_time_use"))
            db_name: str = input(self.json_handler("db_create_name"))
        else:
            print(self.json_handler("db_choose_file"))
            db_name = ""
            while len(db_name) > 12 or not db_name.isalpha():
                db_name: str = input(f"{", ".join(self.files)}: ")
        self.connect_to_db(db_name)

        # Initializes/creates the selected SQL databank and adds all subjects into a list.
        if len(self.subjects) == 0:
            self.create_subjects()
        self.load_subjects()
        self.app_navigator()


    def app_navigator(self) -> None:
        """
        Navigates the app and lets the user edit and manipulate data.
        """
        print(self.json_handler("db_navigation"))
        db_id: int = -1
        while db_id < 0 or db_id >= len(self.subjects):
            try:
                db_id: int = int(input("ID: "))
            except ValueError:
                print("Error: Must be an integer!")

        subj_current: list[super.Cursor] = self.sql_handler(SQLEnum.SUBJECTS)[db_id][0]
        # TODO: Implement navigator


    def create_subjects(self) -> None:
        """
        Creates the study subjects and loads them into code.
        """
        self.json_handler("create_subjects")
        subj_name: str = ""
        subj_time: float = 0.0
        subjects: dict[str, float] = {}

        while True:
            self.json_handler("exit_create_subjects")
            subj_name: str = input("Name: ")
            if subj_name.upper() == "D":    # Done
                break
            if subj_name.upper() == "M":    # Mistake
                rm_key: dict = list(subjects)[-1]
                subjects.pop(rm_key)
            else:
                subj_time = -1.0
                while subj_time < 0.0:
                    try:
                        subj_time: float = float(input("Time (in hours): "))
                    except ValueError:
                        print("Error: Must be a floating point number!")
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


study_time = StudyTime()
