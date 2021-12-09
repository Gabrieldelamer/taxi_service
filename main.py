from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
#from sqlalchemy import ForeignKey

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///taxi_service.sqlite"
db = SQLAlchemy(app)

# db.create_all()

# Создаем описание моделей Базы Данных

class Driver(db.Model):
    __tablename__ = 'driver'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(55), nullable=False)
    car = db.Column(db.String(55), nullable=False)

    def __init__(self, name, car):
        self.name = name
        self.car = car

class Clients(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(55), nullable=False)
    is_vip = db.Column(db.Boolean, nullable=False)

    def __init__(self, name, is_vip):
        self.name = name
        self.is_vip = is_vip

class Orders(db.Model):
    __tablename__ = 'Orders'

    id = db.Column(db.Integer, primary_key=True)
    adress_from = db.Column(db.String(255), nullable=False)
    adress_to = db.Column(db.String(255), nullable=False)
    client_id = db.Column(db.Integer, nullable=False)
    driver_id = db.Column(db.Integer, nullable=False)
    date_created = db.Column(db.DateTime(55), nullable=False)
    status = db.Column(db.String(55), nullable=False)

    def __init__(self, adress_from, adress_to, client_id, driver_id, date_created, status):
        self.adress_from = adress_from
        self.adress_to = adress_to
        self.client_id = client_id
        self.driver_id = driver_id
        self.date_created = date_created
        self.status = status

@app.route('/drivers/<int:id>', methods =['GET'])
def _get_driver(id):
    driver = Driver.query.filter_by(id=id).firs_or404()
    data = {"id": driver.id,
            "name": driver.name,
            "car":driver.car}
    return jsonify(data), 200

@app.route('/drivers', methods =['POST'])
def _add_driver():
    json = request.get_json()
    driver = Driver(name=json.get('name'), car=json.get('car'))
    db.session.add(driver)
    db.session.commit()
    return f"Водитель добавлен с данными: id: {driver.id}", 201

app.run(host='0.0.0.0', port=5000)