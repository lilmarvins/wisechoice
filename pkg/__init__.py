from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate




csrf= CSRFProtect()

def create_app():
    """keep all imports that may cause conflicts within this function so that anytime we write "from debapp... import... none of these statements will be executed" """
    from pkg.models import db
    from pkg import config


    # bring in th instance of the blueprints respectively
    from pkg.admin import adminobj
    from pkg.user import userobj
    from pkg.api import apiobj
    from pkg.error.error import errorbp

    app=Flask(__name__,instance_relative_config=True)


# register the blue print 
    app.register_blueprint(adminobj)
    app.register_blueprint(userobj)
    app.register_blueprint(apiobj)
    app.register_blueprint(errorbp)


    app.config.from_pyfile("config.py", silent=True)
    app.config.from_object(config.ProductionConfig)

    db.init_app(app)
    csrf.init_app(app)
    csrf.exempt(apiobj)
    csrf.exempt(errorbp)
    


    migrate = Migrate(app,db)
    return app

app = create_app()


