from flask_sqlalchemy import SQLAlchemy

from app.enums import UserRole, Orjentacija, Status, FizickoPravnoLice, KupacStatus

db = SQLAlchemy()


class Korisnik (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    role = db.Column(db.Enum(UserRole), nullable=False)


stan_kupac = db.Table('stan_kupac',
                      db.Column('stan_id', db.Integer, db.ForeignKey('stan.id')),
                      db.Column('kupac_id', db.Integer, db.ForeignKey('kupac.id'))
                      )


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


class Kupac(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fizicko_pravno_lice = db.Column(db.Enum(FizickoPravnoLice), nullable=False)
    naziv_ime = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    broj_telefona = db.Column(db.String(100), nullable=False)
    pib_jmbg = db.Column(db.String(50), nullable=False)
    adresa = db.Column(db.String(100), nullable=False)
    datum_prve_posete = db.Column(db.Date)
    kupac_status = db.Column(db.Enum(KupacStatus))
    cena_za_kupca = db.Column(db.DECIMAL, nullable=False)
    napomena = db.Column(db.Text())
    broj_ugovora = db.Column(db.String(100))
    datum_ugovora = db.Column(db.Date)
    id_stanova = db.relationship('Stan', secondary=stan_kupac, backref=db.backref('kupci'))






