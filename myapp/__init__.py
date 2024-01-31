from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():


    from myapp.app.models import Produkt, Transakcja, Saldo

    return app