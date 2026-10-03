"""Find a student with exactly 100 points in every listed subject."""
from Types import DataType


class PerfectStudentFinder:
    def __init__(self, data: DataType) -> None:
        self.data = data

    def find(self) -> str | None:
        for student, subjects in self.data.items():
            if subjects and all(score == 100 for _, score in subjects):
                return student
        return None
