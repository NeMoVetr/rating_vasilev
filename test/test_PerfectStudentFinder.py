import pytest

from src import PerfectStudentFinder, DataType


class TestPerfectStudentFinder:
    def test_init(self) -> None:
        data: DataType = {"Иванов": [("математика", 100)]}
        assert PerfectStudentFinder(data).data is data

    @pytest.mark.parametrize("data, expected", [
        ({}, None),
        ({"Иванов": []}, None),
        ({"Иванов": [("математика", 100)]}, "Иванов"),
        ({"Иванов": [("математика", 100), ("химия", 100)]}, "Иванов"),
        ({"Иванов": [("математика", 100), ("химия", 99)]}, None),
        ({"Иванов": [("математика", 99), ("химия", 100)]}, None),
        ({"Иванов": [("математика", 0), ("химия", 0)]}, None),
        ({"Иванов": [("математика", 101)]}, None),
        ({"Иванов": [("математика", 90), ("химия", 110)]}, None),
        ({"Без оценок": [], "Петров": [("химия", 100)]}, "Петров"),
        ({"Иванов": [("химия", 99)], "Петров": [("химия", 100)]},
         "Петров"),
    ])
    def test_find(self, data: DataType, expected: str | None) -> None:
        assert PerfectStudentFinder(data).find() == expected

    def test_multiple_perfect_students(self) -> None:
        data: DataType = {
            "Иванов": [("математика", 100)],
            "Петров": [("химия", 100)],
        }
        assert PerfectStudentFinder(data).find() == "Иванов"

    def test_repeated_search_does_not_change_data(self) -> None:
        data: DataType = {"Иванов": [("математика", 100)]}
        finder = PerfectStudentFinder(data)
        assert finder.find() == "Иванов"
        assert finder.find() == "Иванов"
        assert data == {"Иванов": [("математика", 100)]}
