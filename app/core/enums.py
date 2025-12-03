from enum import IntEnum, StrEnum


class TokenFields(StrEnum):
    pk_id = 'id'
    user_id = 'user_id'
    username = 'username'
    sub = 'sub'
    exp = 'exp'
    email = 'email'
    role = 'role'
    iat = 'iat'
    is_admin = 'is_admin'
    is_active = 'is_active'
    is_superuser = 'is_superuser'
    organization = 'organization'
    typ = 'typ'


class TokenTypes(StrEnum):
    access = 'access'
    refresh = 'refresh'



class EntityIdRange(IntEnum):
    MIN_ID = 1
    MAX_ID = 32000


class Organizations(StrEnum):
    SDP = 'Spetsdorproject'


class Roles(StrEnum):
    superuser = 'superuser'
    admin = 'admin'
    worker = 'worker'


class RegionCodes(IntEnum):
    MOSCOW77 = 77
    TVER69 = 69
    SAKHALIN65 = 65
    RYBINSK76 = 76
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


class PassportGroups(StrEnum):
    OVIM = 'ОВИМ'
    STROYKONTROL = 'Стройконтроль'
    CODD = 'ЦОДД'
    PTO = 'ПТО'
    _TEST1 = 'test1'
    _TEST2 = 'test2'


class PassportGroupsRoutes(StrEnum):
    OVIM = 'ovim'
    STROYKONTROL = 'stroykontrol'
    CODD = 'codd'
    PTO = 'pto'
    _TEST1 = 'test1'
    _TEST2 = 'test2'
