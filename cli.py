"""
CLI version of the app.
"""
from pandas import DataFrame, concat
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
        user = input(f"Press \"Y\" if you want to add some study time to subject {subj_current}.").upper()
        if user == "Y":
            user = float(input(f"Add the amount of time in minutes.")) / 60.0
            self.sql_handler(SQLEnum.INSERT_SUBJECT_STUDY_TIME, [subj_current[0], user])
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

                deadline: str = input("Would you like to enter a deadline? Y / N\n").upper()
                if deadline == "Y":
                    deadline: str = input("Set Deadline (YYYY-MM-DD): ")
                else:
                    deadline = None
                subjects.update({subj_name: [subj_time, deadline]})

        for subj_name, time_req in subjects.items():
            self.sql_handler(SQLEnum.CREATE_TABLE, subj_name)
            self.sql_handler(SQLEnum.INSERT_SUBJECTS_REQ_TIME, [
                subj_name, time_req[0], time_req[1]])


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
                "Subject": subj_name,
                "Hrs Left": f"{subj_time_left} ({ \
                    subj_time_req})" if subj_time_left != subj_time_req else subj_time_left,
                "Hrs Spent": subj_time_done,
                "Hrs/D": self.statistics_calc("days", subj_time_left, subj_deadline),
                "Hrs/Wk": self.statistics_calc("weeks", subj_time_left, subj_deadline),
                "Hrs/Mo": self.statistics_calc("months", subj_time_left, subj_deadline),
                "Deadline": subj_deadline,
            })
            i += 1
        data_frame: DataFrame = DataFrame(data)
        data_total: list[float] = data_frame[["Hrs Left", "Hrs Spent",
        "Hrs/D", "Hrs/Wk", "Hrs/Mo"]].sum(numeric_only=True)
        data_total_frame = DataFrame([data_total], columns=data_total.index)
        data_total_frame.insert(1, "Subject", "Total")
        data_frame = concat([data_frame, data_total_frame], ignore_index=True)
        print(data_frame)


study_time = StudyTime()
