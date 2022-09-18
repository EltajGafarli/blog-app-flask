from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from app import app,db

from models import Posts,Tag

admin = Admin(app=app)

admin.add_view(ModelView(Posts,db.session,endpoint='/posts'))
admin.add_view(ModelView(Tag,db.session,endpoint='/tags'))
