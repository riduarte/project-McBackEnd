import os
from flask_admin import Admin
from models import db, Cooker, Called, Enterprise
from flask_admin.contrib.sqla import ModelView

class MyModelView(ModelView): 
    column_display_pk = True

def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='4Geeks Admin', template_mode='bootstrap3')
    
    # Add your models here, for example this is how we add a the User model to the admin
    admin.add_view(MyModelView(Cooker, db.session))
    admin.add_view(MyModelView(Called, db.session))
    admin.add_view(MyModelView(Enterprise, db.session))