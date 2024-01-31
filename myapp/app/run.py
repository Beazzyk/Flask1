
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import render_template, redirect, url_for, request

from manager_class import Manager

db = SQLAlchemy()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:\\Users\\domin\\Documents\\kurs_21\\flask_21\\bazka.db'
db.init_app(app)


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


manager = Manager()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/saldo')
def saldo():
    saldo = manager.saldo
    return render_template('saldo.html', saldo=saldo)

@app.route('/sprzedaz', methods=['GET', 'POST'])
def sprzedaz():
    if request.method == 'POST':
        produkt = request.form.get('produkt')
        cena = float(request.form.get('cena'))
        ilosc = int(request.form.get('ilosc'))
        manager.zarejestruj_sprzedaz(produkt, cena, ilosc)

        transakcja = Transakcja(typ='Sprzedaż', produkt_id=produkt, ilosc=ilosc, cena=cena)
        db.session.add(transakcja)
        db.session.commit()


        return redirect(url_for('sprzedaz'))
    else:
        magazyn = manager.magazyn
        return render_template('sprzedaz.html', magazyn=magazyn)


@app.route('/zakup', methods=['GET', 'POST'])
def zakup():
    if request.method == 'POST':
        produkt = request.form.get('produkt')
        cena = float(request.form.get('cena'))
        ilosc = int(request.form.get('ilosc'))
        manager.zarejestruj_zakup(produkt, cena, ilosc)

        transakcja = Transakcja(typ='Zakup', produkt_id=produkt, ilosc=ilosc, cena=cena)
        db.session.add(transakcja)
        db.session.commit()

        return redirect(url_for('index'))
    return render_template('zakup.html')

@app.route('/konto')
def konto():
    return render_template('konto.html', saldo=manager.saldo, magazyn=manager.magazyn)

@app.route('/lista')
def lista():
    return render_template('lista.html', historia=manager.historia_operacji)

@app.route('/stan-magazynu')
def stan_magazynu():
    return render_template('stan_magazynu.html', magazyn=manager.magazyn)

@app.route('/przeglad')
def przeglad():
    return render_template('przeglad.html', saldo=manager.saldo, magazyn=manager.magazyn,
                           historia=manager.historia_operacji)
@app.route('/koniec')
def koniec():
    return "Zakończenie pracy aplikacji."

@app.route('/dodaj-saldo', methods=['GET', 'POST'])
def dodaj_saldo():
    if request.method == 'POST':
        kwota = float(request.form.get('kwota'))
        manager.modyfikuj_saldo_dodaj(kwota)
        return redirect(url_for('saldo'))
    return render_template('dodaj_saldo.html')

@app.route('/odejmij-saldo', methods=['GET', 'POST'])
def odejmij_saldo():
    if request.method == 'POST':
        kwota = float(request.form.get('kwota'))
        manager.modyfikuj_saldo_odejmij(kwota)
        return redirect(url_for('saldo'))
    return render_template('odejmij_saldo.html')



if __name__ == "__main__":
    app.run(debug=True)
