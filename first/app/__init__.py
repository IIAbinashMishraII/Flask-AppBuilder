import logging

from flask import Flask
from flask_appbuilder import AppBuilder, SQLA
from flask_appbuilder.security.sqla.models import PermissionView, Role
from flask_appbuilder import Model

def remove_add_permissions(appbuilder):
    session = appbuilder.get_session()
    all_permissions = session.query(PermissionView).all()
    add_permissions = [perm for perm in all_permissions if 'add' in (perm.permission.name or '').lower()]
    for perm in add_permissions:
        roles = session.query(Role).join(Role.permissions).filter(Role.permissions.contains(perm)).all()
        
        for role in roles:
            if perm in role.permissions:
                role.permissions.remove(perm)
        session.commit()
            
"""
 Logging configuration
"""

logging.basicConfig(format="%(asctime)s:%(levelname)s:%(name)s:%(message)s")
logging.getLogger().setLevel(logging.DEBUG)

app = Flask(__name__)
app.config.from_object("config")
db = SQLA(app)
appbuilder = AppBuilder(app, db.session)


"""
from sqlalchemy.engine import Engine
from sqlalchemy import event

#Only include this for SQLLite constraints
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    # Will force sqllite contraint foreign keys
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()
"""

remove_add_permissions(appbuilder)
from . import views
