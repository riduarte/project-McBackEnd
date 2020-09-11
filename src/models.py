from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import PasswordType


db = SQLAlchemy()

class Cooker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname= db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120),PasswordType(schemes=['pbkdf2_sha512']), unique=False, nullable=False)
    enterprise = db.Column(db.String(100), unique=False, nullable=False)
    name= db.Column(db.String(80), unique=False, nullable=False)
    last_name= db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(),default= True, unique=False, nullable=False) 
    child = db.relationship('Called', lazy=True)

    def __repr__(self):
        return f'<Cooker {self.nickname}>'

    def serialize(self):
        return {
            "id": self.id,
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
        not_edit_file = ["id","enterprise","is_active"]  
        cooker = Cooker.query.get(id)
        for key, value in body.items():
            if key in not_edit_file:
                return "error", 400
            elif key not in not_edit_file:
                setattr(cooker,key,value)       
        db.session.add(cooker)
        db.session.commit()
        return "success",200

    @classmethod
    def add_cooker(cls,new_cooker, email, password):
        new_cooker = cls (
        nickname = cls(email=email, password=password, is_active=True),
        email = new_cooker["email"],
        password = new_cooker["password"],
        enterprise = new_cooker["enterprise"],
        name = new_cooker["name"],
        last_name = new_cooker["last_name"])
        db.session.add(new_cooker)
        db.session.commit()
        return new_cooker

    def delete_cooker(id):
        delete_cooker= Cooker.query.get(id)
        if  delete_cooker.is_active ==  True:
            delete_cooker.is_active= False
            db.session.add(delete_cooker)
            db.session.commit()
            delete_cooker = delete_cooker.serialize()
            return delete_cooker,200
        else:
            return "Error",400

class Called(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    called_code = db.Column(db.String(20), unique=True, nullable=False)
    status = db.Column(db.Enum("espera","listo","entregado","cancelado","proceso"), unique=False, nullable=False)
    time = db.Column(db.Integer, unique=False,nullable=False)
    brand= db.Column(db.String(170), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(),default= True, unique=False, nullable=False)
    parent_id= db.Column(db.Integer, db.ForeignKey('cooker.id'))
   
    #not_edit_file = ["id","brand","is_active"]

    def __repr__(self):
        return f'<Called {self.called_code}>'

    def serialize(self):
        return {
            "id":self.id,
            "called_code": self.called_code,
            "status": self.status,
            "time": self.time,
            "brand":self.brand
        }
    @classmethod  
    def add_called(cls,called_data):    
        called_data = cls(
        called_code = called_data["called_code"],
        status = "espera",
        time = called_data["time"],
        brand = called_data["brand"])
        db.session.add(called_data)
        db.session.commit()

    def get_all_called():
        all_called = Called.query.filter_by( is_active = True)
        all_called = list(map(lambda x: x.serialize(),all_called))
        return all_called

    def get_called(called_id):
        called = Called.query.filter_by(id = called_id).first()
        called = called.serialize()
        return called
    
    def set_called(id, body):
        not_edit_file = ["id","brand","is_active"]  
        called = Called.query.get(id)
        for key, value in body.items():
            if key in not_edit_file:
                return "error", 400
            elif key not in not_edit_file:
                setattr(called,key,value)
        db.session.add(called)
        db.session.commit()
        return "Success",200

    def delete_called(id):
        delete_called = Called.query.get(id)
        if delete_called.is_active == True:
            delete_called.is_active = False
            db.session.add(delete_called)
            db.session.commit()
            delete_called = delete_called.serialize()
            return delete_called,200
        else:
            return "Error",400

class UserOAuth(db.Model, UserMixin):
    id = db.Column(db.String(767), primary_key=True)
    email = db.Column(db.String(767), unique=True, nullable=False)
    name = db.Column(db.Text(), nullable=False)
    profile_pic = db.Column(db.Text(), nullable=False)


    def __init__(self, id_, name, email, profile_pic):
        self.id = id_
        self.name = name
        self.email = email
        self.profile_pic = profile_pic



    @classmethod
    def create(cls, id_, name, email, profile_pic):
        user = cls(id_=id_, name=name, email=email, profile_pic=profile_pic)
        db.session.add(user)
        db.session.commit()
        return user

    def serialize (self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
        }

    @classmethod
    def get(cls, user_id):
        return cls.query.filter_by(id=user_id).one_or_none()