# -*- coding: utf-8 -*-
from src.CalcRating import CalcRating
from src.Types import DataType
import pytest

RatingsType = dict[str, float]


class TestCalcRating:
    @pytest.fixture()
    def input_data(self) -> tuple[DataType, RatingsType]:
        data: DataType = {
            "Абрамов Петр Сергеевич":
                [
                    ("математика", 80),
                    ("русский язык", 76),
                    ("программирование", 100)
                ],
            "Петров Игорь Владимирович":
                [
                    ("математика", 61),
                    ("русский язык", 80),
                    ("программирование", 78),
                    ("литература", 97)
                ]
        }
        rating_scores: RatingsType = {
            "Абрамов Петр Сергеевич": 85.3333,
            "Петров Игорь Владимирович": 79.0000
        }
        return data, rating_scores

    def test_init_calc_rating(
            self, input_data: tuple[DataType, RatingsType]) -> None:
        calc_rating = CalcRating(input_data[0])
        assert input_data[0] == calc_rating.data

    def test_calc(self, input_data: tuple[DataType, RatingsType]) -> None:
        rating = CalcRating(input_data[0]).calc()
        assert rating == pytest.approx(input_data[1], abs=0.001)

    def test_empty_data(self) -> None:
        assert CalcRating({}).calc() == {}

    def test_student_without_subjects(self) -> None:
        assert CalcRating({"Иванов": []}).calc() == {"Иванов": 0.0}

    def test_repeated_calculation(
            self, input_data: tuple[DataType, RatingsType]) -> None:
        calculator = CalcRating(input_data[0])
        calculator.calc()
        assert calculator.calc() == pytest.approx(input_data[1], abs=0.001)
