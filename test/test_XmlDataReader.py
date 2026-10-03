from pathlib import Path
from xml.etree.ElementTree import ParseError

import pytest

from DataReader import DataReader
from src.XmlDataReader import XmlDataReader


@pytest.fixture()
def xml_path(tmp_path: Path) -> Path:
    return tmp_path / "students.xml"


class TestXmlDataReader:
    def test_read(self, xml_path: Path) -> None:
        xml_path.write_text(
            '<?xml version="1.0" encoding="utf-8"?>'
            '<students><!-- Sample data -->'
            '<student name=" Иванов Иван Иванович ">'
            '<subject name=" математика " score="100"/>'
            '<subject name="химия" score="0"/>'
            '</student>'
            '<student name="Петров Петр Петрович">'
            '<subject name="русский язык" score=" 42 "/>'
            '</student>'
            '<student name="Без дисциплин"/>'
            '</students>',
            encoding="utf-8",
        )
        reader = XmlDataReader()
        assert isinstance(reader, DataReader)
        assert reader.read(str(xml_path)) == {
            "Иванов Иван Иванович": [("математика", 100), ("химия", 0)],
            "Петров Петр Петрович": [("русский язык", 42)],
            "Без дисциплин": [],
        }

    def test_empty_students(self, xml_path: Path) -> None:
        xml_path.write_text("<students/>", encoding="utf-8")
        assert XmlDataReader().read(str(xml_path)) == {}

    @pytest.mark.parametrize("xml, message", [
        ("<wrong/>", "root element"),
        ("<students><wrong/></students>", "inside <students>"),
        ("<students><student/></students>", "Missing name"),
        ('<students><student name=" "/></students>', "Missing name"),
        ('<students><student name="A"/><student name=" A "/></students>',
         "Duplicate student"),
        ('<students><student name="A"><wrong/></student></students>',
         "empty <subject>"),
        ('<students><student name="A"><subject name="math" score="100">'
         '<nested/></subject></student></students>', "empty <subject>"),
        ('<students><student name="A"><subject score="100"/>'
         '</student></students>', "Missing name"),
        ('<students><student name="A"><subject name=" " score="100"/>'
         '</student></students>', "Missing name"),
        ('<students><student name="A"><subject name="math" score="100"/>'
         '<subject name=" math " score="90"/></student></students>',
         "Duplicate subject"),
    ])
    def test_invalid_structure(
            self, xml_path: Path, xml: str, message: str) -> None:
        xml_path.write_text(xml, encoding="utf-8")
        with pytest.raises(ValueError, match=message):
            XmlDataReader().read(str(xml_path))

    @pytest.mark.parametrize("score", ["", "abc", "99.5"])
    def test_noninteger_score(self, xml_path: Path, score: str) -> None:
        xml_path.write_text(
            '<students><student name="A">'
            f'<subject name="math" score="{score}"/>'
            '</student></students>', encoding="utf-8",
        )
        with pytest.raises(ValueError, match="Score must be an integer"):
            XmlDataReader().read(str(xml_path))

    def test_missing_score(self, xml_path: Path) -> None:
        xml_path.write_text(
            '<students><student name="A"><subject name="math"/>'
            '</student></students>', encoding="utf-8",
        )
        with pytest.raises(ValueError, match="Score must be an integer"):
            XmlDataReader().read(str(xml_path))

    @pytest.mark.parametrize("score", [-1, 101])
    def test_score_outside_range(self, xml_path: Path, score: int) -> None:
        xml_path.write_text(
            '<students><student name="A">'
            f'<subject name="math" score="{score}"/>'
            '</student></students>', encoding="utf-8",
        )
        with pytest.raises(ValueError, match="between 0 and 100"):
            XmlDataReader().read(str(xml_path))

    def test_malformed_xml(self, xml_path: Path) -> None:
        xml_path.write_text("<students>", encoding="utf-8")
        with pytest.raises(ParseError):
            XmlDataReader().read(str(xml_path))

    def test_missing_file(self, xml_path: Path) -> None:
        with pytest.raises(FileNotFoundError):
            XmlDataReader().read(str(xml_path))

    def test_repeated_reads(self, xml_path: Path) -> None:
        reader = XmlDataReader()
        xml_path.write_text(
            '<students><student name="A"/></students>', encoding="utf-8",
        )
        first_result = reader.read(str(xml_path))
        xml_path.write_text(
            '<students><student name="B"/></students>', encoding="utf-8",
        )
        assert reader.read(str(xml_path)) == {"B": []}
        assert first_result == {"A": []}
