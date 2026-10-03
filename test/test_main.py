# -*- coding: utf-8 -*-
from pathlib import Path
import runpy

import pytest

from src.main import get_path_from_arguments, main


@pytest.fixture()
def correct_arguments_string() -> tuple[list[str], str]:
    return ["-p", "/home/user/file.txt"], "/home/user/file.txt"


@pytest.fixture()
def noncorrect_arguments_string() -> list[str]:
    return ["/home/user/file.txt"]


def test_get_path_from_correct_arguments(
        correct_arguments_string: tuple[list[str], str]) -> None:
    path = get_path_from_arguments(correct_arguments_string[0])
    assert path == correct_arguments_string[1]


def test_get_path_from_noncorrect_arguments(
        noncorrect_arguments_string: list[str]) -> None:
    with pytest.raises(SystemExit) as e:
        get_path_from_arguments(noncorrect_arguments_string)
    assert e.value.code == 2


@pytest.mark.parametrize("args", [[], ["-p"], ["--unknown"]])
def test_missing_or_invalid_arguments(args: list[str]) -> None:
    with pytest.raises(SystemExit) as error:
        get_path_from_arguments(args)
    assert error.value.code == 2


def test_help() -> None:
    with pytest.raises(SystemExit) as error:
        get_path_from_arguments(["--help"])
    assert error.value.code == 0


def test_main_perfect_student(tmp_path: Path, capsys) -> None:
    path = tmp_path / "students.XML"
    path.write_text(
        '<students><student name="Иванов">'
        '<subject name="математика" score="99"/></student>'
        '<student name="Петров"><subject name="математика" score="100"/>'
        '<subject name="химия" score="100"/></student></students>',
        encoding="utf-8",
    )
    assert main(["-p", str(path)]) == 0
    output = capsys.readouterr()
    assert output.out.splitlines()[-1] == (
        "Студент со 100 баллами по всем дисциплинам: Петров"
    )
    assert "Rating:" in output.out
    assert output.err == ""


@pytest.mark.parametrize("xml", [
    "<students/>",
    '<students><student name="Иванов"/></students>',
    '<students><student name="Иванов">'
    '<subject name="математика" score="99"/></student></students>',
])
def test_main_no_perfect_student(tmp_path: Path, capsys, xml: str) -> None:
    path = tmp_path / "students.xml"
    path.write_text(xml, encoding="utf-8")
    assert main(["-p", str(path)]) == 0
    assert capsys.readouterr().out.splitlines()[-1] == (
        "Студентов со 100 баллами по всем дисциплинам нет."
    )


def test_main_text_format(tmp_path: Path, capsys) -> None:
    path = tmp_path / "students.txt"
    path.write_text("Иванов\n математика:100\n химия:100\n", encoding="utf-8")
    assert main(["-p", str(path)]) == 0
    assert capsys.readouterr().out.splitlines()[-1] == (
        "Студент со 100 баллами по всем дисциплинам: Иванов"
    )


@pytest.mark.parametrize("xml", [
    "<students>",
    "<wrong/>",
    '<students><student name="Иванов">'
    '<subject name="математика" score="101"/></student></students>',
])
def test_main_invalid_xml(tmp_path: Path, capsys, xml: str) -> None:
    path = tmp_path / "students.xml"
    path.write_text(xml, encoding="utf-8")
    assert main(["-p", str(path)]) == 1
    output = capsys.readouterr()
    assert output.out == ""
    assert "Ошибка чтения данных:" in output.err


def test_main_missing_file(tmp_path: Path, capsys) -> None:
    assert main(["-p", str(tmp_path / "missing.xml")]) == 1
    assert "Ошибка чтения данных:" in capsys.readouterr().err


def test_main_reads_command_line(tmp_path: Path, capsys, monkeypatch) -> None:
    path = tmp_path / "students.xml"
    path.write_text("<students/>", encoding="utf-8")
    monkeypatch.setattr("sys.argv", ["main.py", "-p", str(path)])
    assert main() == 0
    assert "Студентов со 100 баллами" in capsys.readouterr().out


def test_script_entry_point(tmp_path: Path, capsys, monkeypatch) -> None:
    path = tmp_path / "students.xml"
    path.write_text("<students/>", encoding="utf-8")
    monkeypatch.setattr("sys.argv", ["main.py", "-p", str(path)])
    script = Path(__file__).resolve().parents[1] / "src" / "main.py"
    with pytest.raises(SystemExit) as error:
        runpy.run_path(str(script), run_name="__main__")
    assert error.value.code == 0
    assert "Студентов со 100 баллами" in capsys.readouterr().out
