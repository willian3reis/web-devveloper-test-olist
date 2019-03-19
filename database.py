from flask_sqlalchemy import SQLAlchemy
from appserver import app
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)
manager.add_command('runserver', MigrateCommand)