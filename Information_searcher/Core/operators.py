from enum import Enum


class Operators(Enum):

    @staticmethod
    def list():
        return list(map(lambda c: c.value, Operators))

    AND = "AND"
    OR = "OR"
    NOT = "NOT"