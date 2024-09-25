"""
CLI version of the app.
"""
from datetime import date
from pandas import DataFrame
from script import App, Settings, SQLEnum


class StudyTime(App):
    """
    The app.
    """
    def __init__(self) -> None:
        super().__init__()

        # Initializes/creates SQL file. User can select which one they want to use and name it.
        if self.language == "default":
            select = input(self.json_handler("select_language"))
            self.language = self.json_handler(select, True, Settings.LANGUAGE)

        db_name: str = ""
        if len(self.files) == 0:
            print(self.json_handler("first_time_use"))
            db_name = input(self.json_handler("db_create_name"))
        else:
            print(self.json_handler("db_choose_file"))
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
                print(self.json_handler("error_int"))

        subj_current: list[super.Cursor] = self.sql_handler(SQLEnum.SELECT_SUBJECTS)[db_id][0]
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
            subj_name: str = input("Subject Name: ")
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
                        print(self.json_handler("error_float"))
                subjects.update({subj_name: subj_time})
                #TODO: Add Deadlines
                wants_deadline: bool = input("Would you like to enter a deadline? True / False\n")
                #subjects.update({"deadline": wants_deadline})

        for subj_name, time_req in subjects.items():
            self.sql_handler(SQLEnum.CREATE_TABLE, subj_name)
            self.sql_handler(SQLEnum.INSERT_SUBJECTS_REQ_TIME, [subj_name, time_req])
        self.connection.commit()


    def load_subjects(self) -> None:
        """
        Loads the subjects and stats and formats them.
        """
        data: list = []
        i: int = 0
        for subject in self.subjects:
            subj_name: str = subject[0]
            subj_time_req: float = self.sql_handler(SQLEnum.SELECT_SUBJECTS_REQ_TIME, subj_name)
            subj_time_done: float = self.sql_handler(SQLEnum.SELECT_SUBJECTS_DONE_TIME, subj_name)
            subj_time_done = subj_time_done if subj_time_done is not None else 0.0
            subj_time_left: float = subj_time_req - subj_time_done
            subj_deadline = self.sql_handler(SQLEnum.SELECT_SUBJECTS_DEADLINE, subj_name)

            data.append({
                "ID": i,
                "Subject": subj_name,
                "Hrs Left": f"{subj_time_left} ({subj_time_req})",
                "Hrs Spent": subj_time_done,
                "Hrs/Day": subj_time_left / float((subj_deadline - date.today()).days),
                "Hrs/Week": subj_time_left / float((subj_deadline - date.today()).days) * 7.0,
                "Hrs/Month": subj_time_left / float((subj_deadline - date.today()).days) * 30.0,
                "Deadline": subj_deadline,
            })
            i += 1
        data_frame: DataFrame = DataFrame(data)
        data_frame.set_index("ID", inplace=True)
        data_frame.index.name = "ID"
        print(data_frame)


study_time = StudyTime()
