from flask_sqlalchemy import SQLAlchemy
import bcrypt

db = SQLAlchemy() 

class Enterprise(db.Model):
    __tablename__ = 'enterprise'
    id = db.Column(db.Integer, primary_key=True)
    nickname= db.Column(db.String(80), unique=True, nullable=False)
    name = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(250),unique=False,nullable=True)
    last_name = db.Column(db.String(80), unique=False, nullable=False)
    kitchen_number = db.Column(db.String(80), unique=False, nullable=False)
    hired_hours = db.Column(db.String(80), unique=False, nullable=False)
    enterprise = db.Column(db.String(100), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(),default= True, unique=False, nullable=False)
    #children= db.relationship('Called', lazy=True)
    #cooker_child = db.relationship('Cooker', lazy=True)
    
    def __repr__(self):
        return f'<Enterprise {self.name}>'
    
    def serialize(self):
        return {
            "id": self.id,
            "hired_hours": self.hired_hours,
            "kitchen_number":self.kitchen_number,
            "name":self.name,
            "last_name":self.last_name,
            }

    @classmethod
    def add_enterprise(cls,new_enterprise):
        new_enterprise = cls (
        hired_hours = "horas",
        kitchen_number = 1,
        email = new_enterprise["email"],
        password = bcrypt.hashpw(new_enterprise["password"].encode('utf-8'),bcrypt.gensalt()),
        enterprise = new_enterprise["enterprise"],
        nickname = new_enterprise["nickname"],
        name = new_enterprise["name"],
        last_name = new_enterprise["last_name"])
        db.session.add(new_enterprise)
        db.session.commit()
        return new_enterprise
    
    def get_enterprises():
        all_enterprises = Enterprise.query.filter_by( is_active = True)
        all_enterprises = list(map(lambda x: x.serialize(),all_enterprises))  
        return all_enterprises

class Cooker(db.Model):
    __tablename__ = 'cooker'
    id = db.Column(db.Integer, primary_key=True)
    nickname= db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(250),unique=False,nullable=True)
    company = db.Column(db.String(100), unique=False, nullable=False)
    name= db.Column(db.String(80), unique=False, nullable=False)
    last_name= db.Column(db.String(80), unique=False, nullable=False)
    is_admin = db.Column(db.Boolean(),default= False, unique=False, nullable=False)
    is_active = db.Column(db.Boolean(),default= True, unique=False, nullable=False)
    calleds = db.relationship('Called', backref='Cooker', lazy=True)
    #parent_id= db.Column(db.Integer, db.ForeignKey('enterprise.id'))
    
    def __repr__(self):
        return f'<Cooker {self.nickname}>'
    def serialize(self):
        return {
            "id": self.id,
            "nickname": self.nickname,
            "email": self.email,
            "name":self.name,
            "company": self.company,
            "last_name":self.last_name,
            "is_admin":self.is_admin,
            "calleds":list(map(lambda x: x.serialize(), self.calleds))
        }
    def get_cookers():
        all_cookers= Cooker.query.filter_by( is_active = True)
        all_cookers= list(map(lambda x: x.serialize(),all_cookers))   
        return all_cookers
  
    @staticmethod
    def get_cooker_login(email, password):
        #cooker= Cooker.query.filter_by(email = email).filter_by(password = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())).first()
        cooker= Cooker.query.filter_by(email = email).filter_by(password = password).first()
        return cooker
    
    def get_cooker(cooker_id):
        cooker= Cooker.query.filter_by(id = cooker_id).first()
        cooker = cooker.serialize()
        return cooker
    
    def update_cooker(id, body):
        not_edit_file = ["id","company","is_active"]  
        cooker = Cooker.query.get(id)
        for key, value in body.items():
            if key in not_edit_file:
                return "error", 400
            elif key not in not_edit_file:
                setattr(cooker,key,value)       
        db.session.add(cooker)
        db.session.commit()
        return cooker
    
    @classmethod
    def add_cooker(cls,new_cooker):
        new_cooker = cls (
        email = new_cooker["email"],
        password = bcrypt.hashpw(new_cooker["password"].encode('utf-8'),bcrypt.gensalt()),
        company = new_cooker["company"],
        nickname = new_cooker["nickname"],
        name = new_cooker["name"],
        last_name = new_cooker["last_name"],
        is_admin = False
        )
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
            return delete_cooker
        else:
            return "Error"

class Called(db.Model):
    __tablename__ = 'called'
    id = db.Column(db.Integer, primary_key=True)
    called_code = db.Column(db.String(20), unique=True, nullable=False)
    status = db.Column(db.Enum("espera","listo","entregado","cancelado","proceso"), unique=False, nullable=False)
    time = db.Column(db.String(280), unique=False,nullable=False)
    logo_delivery = db.Column(db.String(280), unique=False, nullable=False)
    room = db.Column(db.String(280), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(),default= True, unique=False, nullable=False)
    cooker_id= db.Column(db.Integer, db.ForeignKey("cooker.id"), nullable=False)
    
   
    def __repr__(self):
        return f'<Called {self.called_code}>'
    
    def serialize(self):
        return {
            "id":self.id,
            "called_code": self.called_code,
            "status": self.status,
            "time": self.time,
            "logo_delivery":self.logo_delivery,
            "room":self.room,
            "cooker_id": self.cooker_id           
        }
   
    @classmethod  
    def add_called(cls,called_data):    
        called_data = cls(
        called_code = called_data["called_code"],
        status = "espera",
        time = called_data["time"],
        logo_delivery = called_data["logo_delivery"],
        room = called_data["room"],
        cooker_id=called_data["cooker_id"]
        )
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
    
    def update_called(id, body):
        not_edit_file = ["id","is_active"]  
        called = Called.query.get(id)
        for key, value in body.items():
            if key in not_edit_file:
                return "error"
            elif key not in not_edit_file:
                setattr(called,key,value)
        db.session.add(called)
        db.session.commit()
        return "Success"
   
    def delete_called(id):
        delete_called = Called.query.get(id)
        if delete_called.is_active == True:
            delete_called.is_active = False
            db.session.add(delete_called)
            db.session.commit()
            delete_called = delete_called.serialize()
            return delete_called
        else:
            return "Error"