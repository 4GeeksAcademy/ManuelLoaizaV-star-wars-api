import os
from flask_admin import Admin
from models import db, Character, Color, Entity, Gender, Planet, User
from flask_admin.contrib.sqla import ModelView

def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='4Geeks Admin', template_mode='bootstrap3')

    admin.add_view(ModelView(Character, db.session))
    admin.add_view(ModelView(Color, db.session))
    admin.add_view(ModelView(Entity, db.session))
    admin.add_view(ModelView(Gender, db.session))
    admin.add_view(ModelView(Planet, db.session))
    admin.add_view(ModelView(User, db.session))
