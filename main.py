from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///taxi_call.db'
db = SQLAlchemy(app)
ma = Marshmallow(app)

"""Models creation"""


class Drivers(db.Model):
    __tablename__ = 'drivers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(55), nullable=False)
    car = db.Column(db.String(55), nullable=False)

    def __init__(self, name, car):
        self.name = name
        self.car = car


class Clients(db.Model):
    __tablename__ = 'clients'
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
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    driver_id = db.Column(db.Integer, db.ForeignKey('drivers.id'), nullable=False)
    date_created = db.Column(db.String(), nullable=False, default=datetime.now())
    status = db.Column(db.String(), nullable=False, default='not_excepted')

    def __init__(self, adress_from, adress_to, client_id, driver_id, date_created, status) -> None:
        self.adress_from = adress_from
        self.adress_to = adress_to
        self.client_id = client_id
        self.driver_id = driver_id
        self.date_created = date_created
        self.status = status


"""Schemas creation"""


class DriversSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Drivers

    name = ma.auto_field()
    car = ma.auto_field()


class ClientsSchema(ma.Schema):
    class Meta:
        fields = ("name", "is_vip")


class OrdersSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Orders

    adress_from = ma.auto_field()
    adress_to = ma.auto_field()
    client_id = ma.auto_field()
    driver_id = ma.auto_field()
    date_created = ma.auto_field()
    status = ma.auto_field()


class OrderUpdateSchema(ma.Schema):
    class Meta:
        fields = ("adress_from", "adress_to")


"""Schemas manifestation"""

drivers_schema = DriversSchema()
clients_schema = ClientsSchema()
orders_schema = OrdersSchema()

"""Drivers methods"""


@app.route('/drivers&id=<int:id>', methods=['GET'])
def get_driver(id):
    get_driver: str = Drivers.query.get(id)
    responce = drivers_schema.jsonify(get_driver)
    if responce.content_length < 5:
        return f"Not Found", 404
    else:
        return responce, 200


@app.route('/drivers', methods=['POST'])
def add_driver():
    name = request.json['name']
    car = request.json['car']
    new_driver = Drivers(name, car)
    db.session.add(new_driver)
    db.session.commit()
    responce = f"Added Driver with Id: {new_driver.id}"
    return jsonify(responce), 201


@app.route('/drivers&id=<int:id>', methods=['DELETE'])
def drop_driver(id):
    drop_driver = Drivers.query.get(id)
    responce_json = drivers_schema.jsonify(drop_driver)
    if responce_json.content_length < 5:
        return f"Not Found", 404
    else:
        db.session.delete(drop_driver)
        db.session.commit()
        responce = drivers_schema.jsonify(drop_driver)
        return responce, 204


"""Clients methods"""


@app.route('/clients&id=<int:id>', methods=['GET'])
def client_get(id):
    get_client = Clients.query.get(id)
    responce = clients_schema.jsonify(get_client)
    if responce.content_length < 5:
        return f"Not Found", 404
    else:
        return responce, 200


@app.route('/clients', methods=['POST'])
def add_client():
    name = request.json['name']
    is_vip = request.json['is_vip']
    new_client = Clients(name, is_vip)
    db.session.add(new_client)
    db.session.commit()
    responce = f"Added client with Id: {new_client.id}"
    return jsonify(responce), 201


@app.route('/drivers&id=<int:id>', methods=['DELETE'])
def drop_client(id):
    drop_client = Clients.query.get(id)
    responce_json = clients_schema.jsonify(drop_client)
    if responce_json.content_length < 5:
        return f"Not Found", 404
    else:
        db.session.delete(drop_client)
        db.session.commit()
        responce = drivers_schema.jsonify(drop_client)
        return responce, 204


"""Orders methods"""


@app.route('/orders', methods=['POST'])
def add_order():
    adress_from = request.json['adress_from']
    if adress_from == '':
        return '{"message":"adress_from value is empty"}', 400
    adress_to = request.json['adress_to']
    if adress_to == '':
        return '{"message":"adress_to value is empty"}', 400
    client_id = request.json['client_id']
    if client_id == '':
        return '{"message":"client_id value is empty"}', 400
    date_created = datetime.now()
    status = 'not_accepted'
    driver_id = request.json['driver_id']
    if driver_id == '':
        return '{"message":"driver_id value is empty"}', 400
    new_order = Orders(adress_from, adress_to, client_id, driver_id, date_created, status)
    db.session.add(new_order)
    db.session.commit()
    responce = f"Added order with Id: {new_order.id}"
    return jsonify(responce), 201


@app.route('/orders&id=<int:id>', methods=['GET'])
def get_order(id):
    get_order = Orders.query.get(id)
    responce = orders_schema.jsonify(get_order)
    if responce.content_length < 5:
        return f"Not Found", 404
    else:
        return responce, 200


@app.route('/orders&id=<int:id>', methods=['PUT'])
def edit_order(id):
    adress_from = request.json['adress_from']
    if adress_from == '':
        return '{"message":"adress_from value is empty"}', 400
    adress_to = request.json['adress_to']
    if adress_to == '':
        return '{"message":"adress_to value is empty"}', 400
    client_id = request.json['client_id']
    if client_id == '':
        return '{"message":"client_id value is empty"}', 400
    status = request.json['status']
    driver_id = request.json['driver_id']
    if driver_id == '':
        return '{"message":"driver_id value is empty"}', 400
    update_order = Orders.query.get(id)
    order_status = update_order.status
    order_atribut = {update_order.client_id, update_order.driver_id, update_order.adress_from, update_order.adress_to}
    order_update_atribut = {client_id, driver_id, adress_from, adress_to}
    if order_status == 'not_accepted' and order_atribut != order_update_atribut:
        return 'ok', 200
    update_order.client_id = client_id
    update_order.driver_id = driver_id
    update_order.adress_from = adress_from
    update_order.adress_to = adress_to
    update_order.date_created = datetime.now()
    db.session.commit()
    if order_status == 'not_accepted' and status == 'in_progress' or status == 'cancelled':
        update_order.status = status
        db.session.commit()
        return 'Status updated', 200
    elif order_status == 'in_progress' and status == 'cancelled' and status == 'done':
        update_order.status = status
        db.session.commit()
        return 'Status updated', 200
    else:
        return 'Error: Status change not allowed', 400


app.run(host='0.0.0.0', port=5000)
