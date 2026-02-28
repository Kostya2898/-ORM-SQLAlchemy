from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pizzeria_flask.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

order_items = db.Table('order_items',
    db.Column('order_id', db.Integer, db.ForeignKey('order.id')),
    db.Column('menu_item_id', db.Integer, db.ForeignKey('menu_item.id'))
)

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    phone_number = db.Column(db.String(15))
    orders = db.relationship('Order', backref='customer')

class MenuItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    price = db.Column(db.Numeric)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    total_price = db.Column(db.Numeric)
    items = db.relationship('MenuItem', secondary=order_items)

with app.app_context():
    db.create_all()

    def add_customer(name, phone):
        customer = Customer(name=name, phone_number=phone)
        db.session.add(customer)
        db.session.commit()
        return customer

    def create_order(customer_id, item_ids):
        items = MenuItem.query.filter(MenuItem.id.in_(item_ids)).all()
        total = sum(item.price for item in items)
        order = Order(customer_id=customer_id, total_price=total)
        order.items = items
        db.session.add(order)
        db.session.commit()
        return order

    def get_customer_orders(customer_id):
        return Order.query.filter_by(customer_id=customer_id).all()