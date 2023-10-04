from enum import Enum as PEnum


class UnitQuantity(str, PEnum):
    ML = "milliliter"
    L = "liter"
    MG = "milligram"
    G = "gram"
    CM = "centimeter"
    M = "meter"
    UNIT = "unit"


class Period(str, PEnum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    ANNUAL = "annual"
