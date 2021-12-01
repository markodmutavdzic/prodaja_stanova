import enum


class UserRole(str, enum.Enum):
    ADMIN = 'ADMIN'
    PRODAVAC = 'PRODAVAC'
    FINANSIJE = 'FINANSIJE'


class Orientation(str, enum.Enum):
    ISTOK = 'ISTOK'
    ZAPAD = 'ZAPAD'
    SEVER = 'SEVER'
    JUG = 'JUG'


class Status(str, enum.Enum):
    SLOBODAN = 'SLOBODAN'
    REZERVISAN = 'REZERVISAN'
    PRODAT = 'PRODAT'


class LegalEntity(str, enum.Enum):
    FIZICKO ='FIZICKO'
    PRAVNO = 'PRAVNO'


class CostumerStatus(str, enum.Enum):
    POTENCIJALNI ='POTECNCIJALNI'
    REZERVISAO = 'REZERVISAO'
    KUPIO = 'KUPIO'



class PaymentMethod(str, enum.Enum):
    KES = 'KES'
    KREDIT = 'KREDIT'
    MESOVITO = 'MESOVITO'

class Order(str, enum.Enum):
    ASC = 'ASC'
    DESC = 'DESC'
