import logging
from flask import Flask
from flask_appbuilder.security.mongoengine.manager import SecurityManager
from flask_appbuilder.security.mongoengine.models import PermissionView, Role
from flask_appbuilder import AppBuilder
from flask_mongoengine import MongoEngine
from flask_appbuilder import Model

"""
 Logging configuration
"""

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(name)s:%(message)s')
logging.getLogger().setLevel(logging.DEBUG)

app = Flask(__name__)
app.config.from_object('config')
app.config['MONGODB_SETTINGS'] = {
    'db': 'mydb',
    'host': 'localhost',
    'port': 27017
}
db = MongoEngine(app)
appbuilder = AppBuilder(app, security_manager_class=SecurityManager)

def remove_add_permissions(appbuilder):
    all_permissions = PermissionView.objects.all()
    add_permissions = [perm for perm in all_permissions if 'add' in (perm.permission.name or '').lower()]
    
    for perm in add_permissions:
        roles = Role.objects(permissions__in=[perm])
        
        for role in roles:
            if perm in role.permissions:
                role.permissions.remove(perm)
                role.save() 

remove_add_permissions(appbuilder)
from app import views

