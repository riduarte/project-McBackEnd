from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class Cooker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nickname= db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    enterprise = db.Column(db.String(100), unique=False, nullable=False)
    name= db.Column(db.String(80), unique=False, nullable=False)
    last_name= db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(),default= True, unique=False, nullable=False) 
    child = db.relationship('Called', lazy=True)

    def __repr__(self):
        return f'<Cooker {self.nickname}>'

    def serialize(self):
        return {
            "nickname": self.nickname,
            "email": self.email,
            "password":self.password,
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
   
    @classmethod
    def add_cooker(cls,new_cooker):
        new_cooker = cls (
        nickname = new_cooker["nickname"],
        email = new_cooker["email"],
        password = new_cooker["password"],
        enterprise = new_cooker["enterprise"],
        name = new_cooker["name"],
        last_name = new_cooker["last_name"])

        db.session.add(new_cooker)
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
    is_active = db.Column(db.Boolean(),default= True, unique=False, nullable=False)
    parent_id= db.Column(db.Integer, db.ForeignKey('cooker.id'))

    def __repr__(self):
        return f'<Called {self.called_code}>'

    def serialize(self):
        return {
            "called_code": self.called_code,
            "id": self.id,
            "status": self.status,
            "time": self.time,
            "brand":self.brand,
            "is_active":self.is_active
        }
    @classmethod  
    def add_called(cls,called_data):    
        called_data = cls(
        called_code = called_data["called_code"],
        status = called_data["status"],
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
        called= Called.query.get(id)
        for key, value in body.items():
            if key != "id":
                setattr(called,key,value)

        db.session.commit()

    def delete_called(id):
        delete_called = Called.query.get(id)
        delete_called.is_active = False
        db.session.commit()
