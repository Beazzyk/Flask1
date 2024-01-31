from run import db



class Produkt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nazwa = db.Column(db.String(50), unique=True, nullable=False)
    cena = db.Column(db.Float, nullable=False)
    ilosc_w_magazynie = db.Column(db.Integer, nullable=False)


class Transakcja(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    typ = db.Column(db.String(50), nullable=False)
    produkt_id = db.Column(db.Integer, db.ForeignKey('produkt.id'), nullable=False)
    ilosc = db.Column(db.Integer, nullable=False)
    cena = db.Column(db.Float, nullable=False)
    data = db.Column(db.DateTime, default=db.func.current_timestamp())

class Saldo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    kwota = db.Column(db.Float, nullable=False, default=0.0)