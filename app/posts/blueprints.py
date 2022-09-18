from flask import Blueprint
from flask import render_template


posts = Blueprint('posts',__name__,template_folder='templates',url_prefix='/posts')


# from .admin import admin,ModelView
# from models import Posts
from app import db
# from flask_security import current_user,login_required, RoleMixin, Security 
# from flask_security import SQLAlchemyUserDatastore,UserMixin,utils


# admin.add_view(ModelView(Posts, db.session, category="Team"))

from . import routes