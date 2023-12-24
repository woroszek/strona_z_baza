from flask import Flask, render_template, request, redirect
from flask_alembic import Alembic
import func
from func import manager, db
from app import app


@app.route('/')
def index():
    func.db_create()
    balance = func.Balance.query.first().balance
    komunikat = manager.komunikat
    history = func.Product.query.all()
    return render_template('page.html', balance=balance, komunikat=komunikat, history=history)


@app.route("/purchase", methods=["POST"])
def purchase_view():
    try:
        name = request.form.get("item")
        quantity = int(request.form.get("quantity"))
        cost = int(request.form.get("cost"))
        product = func.Product(name=name, quantity=quantity, cost=cost)
        func.purchase(product)
    except ValueError:
        manager.komunikat = 'Uzupełnij wszystkie pola formularzu.'
    return redirect('/')


@app.route("/sell", methods=["POST"])
def sell_view():
    try:
        name = request.form.get("item")
        quantity = int(request.form.get("quantity"))
        cost = int(request.form.get("cost"))
        product = func.Product(name=name, quantity=quantity, cost=cost)
        func.sell(product)
    except ValueError:
        manager.komunikat = 'Uzupełnij wszystkie pola formularzu.'
    return redirect('/')


@app.route("/balance", methods=["POST"])
def balance():
    try:
        add = request.form.get("add")
        func.change_balance(int(add))
        manager.komunikat = f"Zmieniono saldo o {add}"
        historyy = func.History(text=f"Zmieniono saldo o {add}")
        db.session.add(historyy)
        db.session.commit()
    except ValueError:
        manager.komunikat = 'Uzupełnij pole formularzu.'
    return redirect('/')


@app.route('/history.html')
def history():
    history_a = ''
    komunikat = ''
    return render_template("history.html", history_a=history_a, komunikat=komunikat)


@app.route('/history', methods=["POST"])
def history_view():
    history_a = func.History.query.all()
    try:
        od = int(request.form.get("Od"))
        do = int(request.form.get("Do"))
        if not history_a :
            manager.komunikat = "Historia jest pusta."
        elif history_a and do >= od > 0:
            history_b = history_a[od-1:do]
            history_a = history_b
            manager.komunikat = "Wyświetlam historię."
        else:
            manager.komunikat = "Podano nieprawidlowe dane. Program wyświetli całą historię."
    except ValueError:
        if history_a:
            manager.komunikat = "Podano nieprawidlowe dane. Program wyświetli całą historię."
            history_a = func.History.query.all()
        else:
            manager.komunikat = "Historia jest pusta."
    return render_template("history.html", history_a=history_a, komunikat=manager.komunikat)


alembic = Alembic()
alembic.init_app(app)

if __name__ == "__main__":
    app.run(debug=True)
