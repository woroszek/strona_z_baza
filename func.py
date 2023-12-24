from flask_sqlalchemy import SQLAlchemy
from app import app

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'  # test db to nazwa pliku w którym utworzymy bazę danych
db = SQLAlchemy(app)


class Balance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    balance = db.Column(db.Integer, nullable=False)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    cost = db.Column(db.Integer, nullable=False)

class History(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(120), nullable=False)


def db_create():
    db.create_all()
    balance = Balance.query.first()
    if not balance:
        initial_balance = Balance(balance=0)
        db.session.add(initial_balance)
        db.session.commit()


def change_balance(add):
    balance = Balance.query.first().balance
    if balance + add < 0:
        manager.komunikat = "Saldo nie może być ujemne."
    else:
        Balance.query.first().balance += add
        db.session.commit()
        return True


def purchase(product: Product):
    balance = Balance.query.first().balance
    if balance >= product.quantity * product.cost:
        is_product = Product.query.filter_by(name=product.name).first()
        if is_product and product.cost == is_product.cost:
            change_balance(-product.quantity * product.cost)
            manager.komunikat = f"Dodano produkt {product.name} w ilości {product.quantity} w cenie {product.cost}"
            is_product.quantity += product.quantity
            historyy = History(text=f"Dodano produkt {product.name} w ilości {product.quantity} w cenie {product.cost}")
            db.session.add(historyy)
            db.session.commit()
        elif is_product and product.cost != is_product.cost:
            manager.komunikat = "Próbujesz dodać ten sam produkt w innej cenie."
        else:
            manager.komunikat = f"Dodano produkt {product.name} w ilości {product.quantity} w cenie {product.cost}"
            historyy = History(text=f"Dodano produkt {product.name} w ilości {product.quantity} w cenie {product.cost}")
            db.session.add(historyy)
            db.session.add(product)
            db.session.commit()
            change_balance(-product.quantity * product.cost)
        return True
    else:
        manager.komunikat = "Brak środków na pokrycie zakupu."
        return False


def sell(product: Product):
    is_product = Product.query.filter_by(name=product.name).first()
    if is_product:
        if is_product.quantity >= product.quantity:
            change_balance(product.quantity * product.cost)
            is_product.quantity -= product.quantity
            manager.komunikat = f"Sprzedano produkt {product.name} w ilości {product.quantity} w cenie {product.cost}"
            historyy = History(text=f"Sprzedano produkt {product.name} w ilości {product.quantity} w cenie {product.cost}")
            db.session.add(historyy)
            db.session.commit()
            if is_product.quantity == 0:
                db.session.delete(is_product)
                db.session.commit()
        else:
            manager.komunikat = "Próbujesz sprzedać więcej produktów niż mamy na magazynie."
    else:
        manager.komunikat = "Nie mamy podanego produktu w magazynie."


class Manager:
    def __init__(self):
        self.komunikat = "Tutaj zobaczysz komunikaty."

manager = Manager()
