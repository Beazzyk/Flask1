
from . import app
from flask import render_template, redirect, url_for, request
from myapp import db
from myapp.app.manager_class import Manager
from myapp.app.models import Transakcja

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