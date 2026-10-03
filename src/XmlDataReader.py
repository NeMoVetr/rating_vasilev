"""Read student names and scores from the laboratory XML format."""
from xml.etree import ElementTree

from DataReader import DataReader
from Types import DataType


class XmlDataReader(DataReader):
    def read(self, path: str) -> DataType:
        root = ElementTree.parse(path).getroot()
        if root.tag != "students":
            raise ValueError("Expected <students> as the root element")

        students: DataType = {}
        for student in root:
            if student.tag != "student":
                raise ValueError("Expected <student> inside <students>")
            name = self._read_name(student)
            if name in students:
                raise ValueError(f"Duplicate student: {name}")

            subjects: list[tuple[str, int]] = []
            subject_names: set[str] = set()
            for subject in student:
                if subject.tag != "subject" or len(subject):
                    raise ValueError("Expected an empty <subject> element")
                subject_name = self._read_name(subject)
                if subject_name in subject_names:
                    raise ValueError(f"Duplicate subject: {subject_name}")
                try:
                    score = int(subject.get("score", ""))
                except ValueError as error:
                    raise ValueError("Score must be an integer") from error
                if not 0 <= score <= 100:
                    raise ValueError("Score must be between 0 and 100")
                subjects.append((subject_name, score))
                subject_names.add(subject_name)
            students[name] = subjects
        return students

    @staticmethod
    def _read_name(element: ElementTree.Element) -> str:
        name = element.get("name", "").strip()
        if not name:
            raise ValueError(f"Missing name in <{element.tag}>")
        return name
