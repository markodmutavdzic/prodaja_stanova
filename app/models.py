from flask_sqlalchemy import SQLAlchemy

from app.enums import UserRole, Orjentacija, Status, FizickoPravnoLice, \
    KupacStatus, Valuta, NacinPlacanja

db = SQLAlchemy()


class Korisnik (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ime = db.Column(db.String(50), nullable=False)
    prezime = db.Column(db.String(50), nullable=False)
    korisnicko_ime = db.Column(db.String(50), nullable=False)
    lozinka = db.Column(db.String(50), nullable=False)
    role = db.Column(db.Enum(UserRole), nullable=False)


class Stan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lamela = db.Column(db.String(50))
    kvadratura = db.Column(db.DECIMAL, nullable=False)
    sprat = db.Column(db.String(50), nullable=False)
    broj_soba = db.Column(db.DECIMAL, nullable=False)
    orjentisanost = db.Column(db.Enum(Orjentacija))
    broj_terasa = db.Column(db.Integer, nullable=False)
    cena = db.Column(db.DECIMAL, nullable=False)
    status = db.Column(db.Enum(Status), default=Status.SLOBODAN)
    novogradnja = db.Column(db.Boolean)
    u_izgradnji = db.Column(db.Boolean)
    useljiv_od = db.Column(db.Date)


class Kupac(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fizicko_pravno_lice = db.Column(db.Enum(FizickoPravnoLice), nullable=False)
    naziv_ime = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    broj_telefona = db.Column(db.String(100), nullable=False)
    pib_jmbg = db.Column(db.String(50), nullable=False)
    mesto = db.Column(db.String(100), nullable=False)
    ulica = db.Column(db.String(100), nullable=False)
    broj = db.Column(db.String(100), nullable=False)
    datum_prve_posete = db.Column(db.Date)


class StanKupac(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    stan_id = db.Column(db.Integer,db.ForeignKey('stan.id'))
    kupac_id = db.Column(db.Integer,db.ForeignKey('kupac.id'))
    kupac_status = db.Column(db.Enum(KupacStatus))
    cena_za_kupca = db.Column(db.DECIMAL)
    odobrena_cena = db.Column(db.Boolean)
    napomena = db.Column(db.Text())
    valuta = db.Column(db.Enum(Valuta))
    nacin_placanja = db.Column(db.Enum(NacinPlacanja))
    iznos_kapare = db.Column(db.DECIMAL)
    rok_ugovor = db.Column(db.Date)
    banka = db.Column(db.String(50))
    iznos_kredita = db.Column(db.DECIMAL)
    iznos_kes_uplate = db.Column(db.DECIMAL)
    broj_ugovora = db.Column(db.String(100))
    datum_ugovora = db.Column(db.Date)











