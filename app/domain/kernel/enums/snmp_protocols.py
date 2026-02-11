from enum import StrEnum


class SnmpProtocols(StrEnum):
    SWARCO_STCIP = "swarco_stcip"
    POTOK_STCIP = "potok_stcip"
    POTOK_UG405 = "potok_ug405"
    SIGNAL_STCIP = "signal_stcip"
    PEEK = "UG405"