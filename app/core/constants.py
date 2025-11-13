from enum import IntEnum, StrEnum


class RegionCodes(IntEnum):
    MOSCOW77 = 77
    TVER = 69
    SAKHALIN = 65
    RYBINSK = 76
    TMUTARAKAN1111 = 1111


class RegionNames(StrEnum):
    MOSCOW = 'Москва'
    TVER = 'Тверь'
    SAKHALIN = 'Сахалин'
    RYBINSK = 'Рыбинск'
    TMUTARAKAN = 'Тмутаракань'


class ServiceOrganizations(StrEnum):
    CODD = 'ЦОДД'


class Districts(StrEnum):
    CENTRAL = 'ЦАО'
    WEST = 'ЗАО'
    EAST = 'ВАО'
    SOUTH = 'ЮАО'


class PassportsOwners(StrEnum):
    OVIM = 'овим'
    STROYKONTROL = 'стройконтроль'
