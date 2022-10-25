from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from os import path
from datetime import datetime, date
from sqlalchemy import desc

db = SQLAlchemy()
DB_NAME = "database.db"


class Coop(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    location = db.Column(db.String)
    fish = db.Column(db.String)
    weight = db.Column(db.Integer)
    price = db.Column(db.Integer)
    boat = db.Column(db.Integer)
    boat_fishnet = db.Column(db.Integer)
    cycle = db.Column(db.Integer)
    boat_paragat = db.Column(db.Integer)
    fish_rod = db.Column(db.Integer)
    boat_both_f_p = db.Column(db.Integer)
    day = db.Column(db.Integer)
    month = db.Column(db.Integer)
    year = year = db.Column(db.Integer)
    project = db.Column(db.String)
    income = db.Column(db.Integer)
    created_when = db.Column(db.DateTime(timezone=True), default=func.now())
    deleted = db.Column(db.Integer, default=0)

    def __init__(self, date, location, fish, weight, price, boat, boat_fishnet, cycle, boat_paragat,
                 fish_rod, boat_both_f_p, day, month, year, project, income):
        self.date = date
        self.location = location
        self.fish = fish
        self.weight = weight
        self.price = price
        self.boat = boat
        self.boat_fishnet = boat_fishnet
        self.cycle = cycle
        self.boat_paragat = boat_paragat
        self.fish_rod = fish_rod
        self.boat_both_f_p = boat_both_f_p
        self.day = day
        self.month = month
        self.year = year
        self.project = project
        self.income = income

# DEFINITIONS
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)
    create_database(app)
    return app


def create_database(app):
    if not path.exists('flaskCRUD/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database')


# APP
app = create_app()


# ROUTES
@app.route('/')
def Index():
    all_coop = db.session.query(Coop).filter(Coop.deleted == 0).order_by(desc(Coop.id))
    today = date.today()
    location = ['Gocek', 'Gokova', 'Calis']
    species = ['Akya', 'Palamut', 'Mercan']
    project = ['Sonrası', 'Öncesi']

    return render_template("index.html", coops=all_coop, today=today, location=location, species=species, project=project)


@app.route('/insert', methods=['POST'])
def insert():
    if request.method == 'POST':

        date = datetime.strptime(request.form['Date'], '%Y-%m-%d')
        location = request.form.get('Location', type=str)
        fish = request.form.get('Fish', type=str)
        weight = request.form.get('Weight', type=float)
        price = request.form.get('Price', type=float)
        boat = request.form.get('Boat', type=int)
        boat_fishnet = request.form.get('Boat_fishnet', type=int)
        cycle = request.form.get('Cycle', type=int)
        boat_paragat = request.form.get('Boat_paragat', type=int)
        fish_rod = request.form.get('Fish_rod', type=int)
        boat_both_f_p = request.form.get('Boat_both_f_p', type=int)
        day = request.form.get('Day', type=int)
        month = request.form.get('Month', type=int)
        year = request.form.get('Year', type=int)
        project = request.form.get('Project', type=str)
        income = weight*price
        income = float("{:.2f}".format(income))

        new_coop = Coop(date=date, day=day, month=month, year=year, location=location, fish=fish, weight=weight,
                        price=price, boat=boat, boat_fishnet=boat_fishnet, cycle=cycle, boat_paragat=boat_paragat,
                        fish_rod=fish_rod, boat_both_f_p=boat_both_f_p, project=project, income=income)
        db.session.add(new_coop)
        db.session.commit()
        flash("Veri Eklendi!")

        return redirect(url_for('Index'))

@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':
        updated_coop = Coop.query.get(request.form.get('id'))

        updated_coop.date = datetime.strptime(request.form['editDate'], '%Y-%m-%d')
        updated_coop.location = request.form['editLocation']
        updated_coop.fish = request.form['editFish']
        updated_coop.weight = request.form['editWeight']
        updated_coop.price = request.form['editPrice']
        updated_coop.boat = request.form['editBoat']
        updated_coop.boat_fishnet = request.form['editBoat_fishnet']
        updated_coop.cycle = request.form['editCycle']
        updated_coop.boat_paragat = request.form['editBoat_paragat']
        updated_coop.fish_rod = request.form['editFish_rod']
        updated_coop.boat_both_f_p = request.form['editBoat_both_f_p']

        db.session.commit()
        flash("Data is updated!")

        return redirect(url_for('Index'))

@app.route('/delete/<id>/', methods=['GET', 'POST'])
def delete(id):
    deleted_coop = Coop.query.get(id)
    deleted_coop.deleted = 1
    db.session.commit()

    return redirect(url_for('Index'))

# RUN
if __name__ == "__main__":
    app.run(debug=True)  ## development state true then remove
