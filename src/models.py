from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

db = SQLAlchemy()

class Cooker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname= db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    enterprise = db.Column(db.String(100), unique=False, nullable=False)
    name= db.Column(db.String(80), unique=False, nullable=False)
    last_name= db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    order = db.relationship('Order', lazy=True)

    def __repr__(self):
        return f'<Cooker {self.nickname}>'

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "enterprise":self.enterprise,
            "name":self.name,
            "last_name":self.last_name
        }
    def getUsers():
        all_cookers= Cooker.query.all()
        all_cookers = list(map(lambda x: x.serialize(), all_cookers))
        return all_cookers
    
    def getUser(cooker_id):
        cooker= Cooker.query.filter_by(id = cooker_id).first()
        cooker = cooker.serialize()
        return cooker
    
    def addCooker(cooker_data):
        cooker_new= Cooker()
        cooker_new.nickname = cooker_data["nickname"]
        cooker_new.email = cooker_data["email"]
        cooker_new.password = cooker_data["password"]
        cooker_new.enterprise = cooker_data["enterprise"]
        cooker_new.name = cooker_data["name"]
        cooker_new.last_name = cooker_data["last_name"]
        cooker_new.is_active= cooker_data["is_active"]

        db.session.add(cooker_new)
        db.session.commit()
   
    def deleteCooker(id):
        delete_cooker= Cooker.query.get(id)
        db.session.delete(delete_cooker)
        db.session.commit()

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_code = db.Column(db.String(20), unique=True, nullable=False)
    status = db.Column(db.String(80), unique=False, nullable=False)
    time = db.Column(db.Integer, unique=False,nullable=False)
    brand= db.Column(db.String(170), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    cooker_id= db.Column (db.Integer, db.ForeignKey ('cooker.id'))

    def __repr__(self):
        return f'<Order {self.order_code}>'

    def serialize(self):
        return {
            "id": self.id,
            "status": self.status,
            "time": self.time,
            "brand":self.brand
        }
        
    def addOrder(order_data):
        order_new= Order()
        order_new.order_code = order_data["order_code"]
        order_new.status = order_data["status"]
        order_new.time= order_data["time"]
        order_new.brand = order_data["brand"]
        order_new.is_active= order_data["is_active"]
        
        db.session.add(order_new)
        db.session.commit()

    def getOrders():
        all_orders= Order.query.all()
        all_orders = list(map(lambda x: x.serialize(), all_orders))
        return all_orders

    def getOrder(order_id):
        order= Order.query.filter_by(id = order_id).first()
        order= order.serialize()
        return order

    def deleteOrder(id):
        delete_order= Order.query.get(id)
        db.session.delete(delete_order)
        db.session.commit()
