# -*- coding: utf-8 -*-
import argparse
import sys
from xml.etree.ElementTree import ParseError

from CalcRating import CalcRating
from PerfectStudentFinder import PerfectStudentFinder
from TextDataReader import TextDataReader
from XmlDataReader import XmlDataReader


def get_path_from_arguments(args) -> str:
    parser = argparse.ArgumentParser(description="Path to datafile")
    parser.add_argument("-p", dest="path", type=str, required=True,
                        help="Path to datafile")
    args = parser.parse_args(args)
    return args.path


def main(args: list[str] | None = None) -> int:
    path = get_path_from_arguments(sys.argv[1:] if args is None else args)
    reader = (
        XmlDataReader() if path.lower().endswith(".xml") else TextDataReader()
    )
    try:
        students = reader.read(path)
    except (OSError, ValueError, ParseError) as error:
        print(f"Ошибка чтения данных: {error}", file=sys.stderr)
        return 1
    print("Students: ", students)
    rating = CalcRating(students).calc()
    print("Rating: ", rating)
    student = PerfectStudentFinder(students).find()
    if student is None:
        print("Студентов со 100 баллами по всем дисциплинам нет.")
    else:
        print(f"Студент со 100 баллами по всем дисциплинам: {student}")
    return 0


if __name__ == "__main__":
    main()
