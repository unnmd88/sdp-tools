from enum import StrEnum


class ControllerTypes(StrEnum):
    SWARCO = "swarco"
    POTOK = "potok"
    PEEK = "peek"
    SIGNAL = "signal"
    DKS = "dks"
    SICE = "sice"