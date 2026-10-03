# -*- coding: utf-8 -*-
from Types import DataType
from DataReader import DataReader


class TextDataReader(DataReader):
    def __init__(self) -> None:
        self.key: str = ""
        self.students: DataType = {}

    def read(self, path: str) -> DataType:
        with open(path, encoding='utf-8') as file:
            for line in file:
                if not line.startswith(" "):
                    self.key = line.strip()
                    self.students[self.key] = []

                else:
                    subj, score = line.split(":", maxsplit=1)
                    student_score = (subj.strip(), int(score.strip()))
                    self.students[self.key].append(student_score)
        return self.students
