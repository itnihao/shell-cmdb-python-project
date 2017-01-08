# -*- coding: utf-8 -*-
from application import app, assets_env,db
from flask.ext.script import Manager,Shell
from flask.ext.script import Server
from flask.ext.assets import ManageAssets
from models.user import User
from models.user_role import UserRole
import web
from flask_socketio import SocketIO
import celery
from flask.ext.migrate import Migrate, MigrateCommand

# socketio=SocketIO(app)

manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('runserver', Server(host='0.0.0.0', port=app.config.get('SERVER_PORT'), use_debugger=True))
manager.add_command('assets', ManageAssets(assets_env))

def make_shell_context():
    return dict(app=app, db=db, User=User, UserRole=UserRole)
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)
# manager.add_command("runserver", socketio.run(
#    app,
#    host='0.0.0.0',
#    port=app.config.get('SERVER_PORT'),
#    use_reloader=False,
#    debug=True)
# )


@manager.command
def create_data():
    """create all database tables"""
    with app.app_context():
        from application import db
        import models
        db.create_all()

@manager.command
def update_data():
    """create all database tables"""
    with app.app_context():
        from application import db
        import models
        db.reflect()


def main():
    manager.run()

if __name__ == '__main__':

    try:
        import sys
        sys.exit(main())
    except Exception as e:
        print e

__all__ = []