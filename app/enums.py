import enum


class UserRole(enum.Enum):
    ADMIN = 'ADMIN'
    PRODAVAC = 'PRODAVAC'
    FINANSIJE = 'FINANSIJE'

class Orjentacija(enum.Enum):
    ISTOK = 'ISTOK'
    ZAPAD = 'ZAPAD'
    SEVER = 'SEVER'
    JUG = 'JUG'

class Status(enum.Enum):
    SLOBODAN = 'SLOBODAN'
    REZERVISAN = 'REZERVISAN'
    PRODAT = 'PRODAT'


class FizickoPravnoLice(enum.Enum):
    FIZICKO ='FIZICKO'
    PRAVNO = 'PRAVNO'

class KupacStatus(enum.Enum):
    POTENCIJALNI ='POTECNCIJALNI'
    REZERVISAO = 'REZERVISAO'
    KUPIO = 'KUPIO'