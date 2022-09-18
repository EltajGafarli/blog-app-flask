from flask import Flask
from config import Config
from devtools import debug

from flask_sqlalchemy import SQLAlchemy

from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand

from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


from flask_security import SQLAlchemyUserDatastore
from flask_security import Security


app = Flask(__name__) 
app.secret_key = Config.SECRET_KEY
app.config.from_object(Config)



db = SQLAlchemy(app=app)




migrate = Migrate(app=app,db=db)
manager = Manager(app=app)
manager.add_command('db',MigrateCommand)

from models import User,Role
from admin import admin


user_datastore = SQLAlchemyUserDatastore(db,User,Role)

security = Security(app,user_datastore)






