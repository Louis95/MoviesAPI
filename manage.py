from models import db,set_up_db
from app import create_app
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand


app = create_app()
set_up_db(app)
app.config.from_object('config')
migrate = Migrate(app, db)
manager = Manager(app=app)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
