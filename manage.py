from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import create_app
from models import db, Magician, Show

app = create_app()

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


@manager.command
def seed():
    Show(show_name='The Prisoner of Azkaban', show_date='2010-01-01').insert()
    Show(show_name='Chamber of Secerets', show_date='2015-01-01').insert()

    Magician(name='Harry Potter', age=15, gender='male').insert()
    Magician(name='Dumbledore', age=50, gender='male').insert()


if __name__ == '__main__':
    manager.run()