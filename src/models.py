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
    is_active = db.Column(db.Boolean(True), unique=False, nullable=False) 
    child = db.relationship('Order', lazy=True)

    def __repr__(self):
        return f'<Cooker {self.nickname}>'

    def serialize(self):
        return {
            "nickname": self.nickname,
            "email": self.email,
            "enterprise":self.enterprise,
            "name":self.name,
            "last_name":self.last_name,
        }
    def get_users():
        all_cookers= Cooker.query.filter_by( is_active = True)
        all_cookers= list(map(lambda x: x.serialize(),all_cookers))
        return all_cookers
    
    def get_user(cooker_id):
        cooker= Cooker.query.filter_by(id = cooker_id).first()
        cooker = cooker.serialize()
        return cooker
    
    def set_user(id, body):
        cooker= Cooker.query.get(id)
        for key, value in body.items():
            if key != "id":
                setattr(cooker,key,value)

        db.session.commit()
   
    def add_cooker(cooker_data):
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

   
    def delete_cooker(id):
        delete_cooker= Cooker.query.get(id)
        delete_cooker.is_active= False
        db.session.commit()

class Called(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    called_code = db.Column(db.String(20), unique=True, nullable=False)
    status = db.Column(db.String(80), unique=False, nullable=False)
    time = db.Column(db.Integer, unique=False,nullable=False)
    brand= db.Column(db.String(170), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(True), unique=False, nullable=False)
    parent_id= db.Column(db.Integer, db.ForeignKey('cooker.id'))

    def __repr__(self):
        return f'<Called {self.order_code}>'

    def serialize(self):
        return {
            "id": self.id,
            "status": self.status,
            "time": self.time,
            "brand":self.brand
        }
        
    def add_called(order_data):
        called_new= Called()
        called_new.called_code = called_data["called_code"]
        called_new.status = called_data["status"]
        called_new.time= called_data["time"]
        called_new.brand = called_data["brand"]
        called_new.is_active= called_data["is_active"]
        
        db.session.add(called_new)
        db.session.commit()

    def get_all_called():
        all_called = Called.query.filter_by( is_active = True).first()
        all_called = all_orders.serialize()
        return all_called


    def get_called(called_id):
        called = Called.query.filter_by(id = called_id).first()
        called = called.serialize()
        return called

    def set_called(id, body):
        called= Called.query.get(id)
        for key, value in body.items():
            if key != "id":
                setattr(called,key,value)

        db.session.commit()

    def delete_called(id):
        delete_called = Called.query.get(id)
        delete_called.is_active = False
        db.session.commit()
