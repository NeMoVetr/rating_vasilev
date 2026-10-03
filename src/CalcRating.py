# -*- coding: utf-8 -*-
from Types import DataType

RatingType = dict[str, float]

# This intentionally long comment is used to demonstrate how CI reports a style error in the source code.


class CalcRating:
    def __init__(self, data: DataType) -> None:
        self.data: DataType = data
        self.rating: RatingType = {}

    def calc(self) -> RatingType:
        for key, subjects in self.data.items():
            self.rating[key] = (
                sum(score for _, score in subjects) / len(subjects)
                if subjects else 0.0
            )
        return self.rating
