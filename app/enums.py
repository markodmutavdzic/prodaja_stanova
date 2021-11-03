import enum


class UserRole(enum.Enum):
    ADMIN = 'ADMIN'
    PRODAVAC = 'PRODAVAC'
    FINANSIJE = 'FINANSIJE'


class Orientation(enum.Enum):
    ISTOK = 'ISTOK'
    ZAPAD = 'ZAPAD'
    SEVER = 'SEVER'
    JUG = 'JUG'


class Status(enum.Enum):
    SLOBODAN = 'SLOBODAN'
    REZERVISAN = 'REZERVISAN'
    PRODAT = 'PRODAT'


class LegalEntity(enum.Enum):
    FIZICKO ='FIZICKO'
    PRAVNO = 'PRAVNO'


class CostumerStatus(enum.Enum):
    POTENCIJALNI ='POTECNCIJALNI'
    REZERVISAO = 'REZERVISAO'
    KUPIO = 'KUPIO'


class Currency(enum.Enum):
    EUR = 'EUR'
    RSD = 'RSD'


class PaymentMethod(enum.Enum):
    KES = 'KES'
    KREDIT = 'KREDIT'
    MESOVITO = 'MESOVITO'
