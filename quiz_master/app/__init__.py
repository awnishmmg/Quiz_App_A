from flask import Flask
 
def create_app():
    app = Flask(__name__)
    app.secret_key  = 'Your_Secret_key'

    #Set Application Context Manager
    with app.app_context():
        from app.models import initialise_db,create_admin
        initialise_db() #create Tables.

        # Admin Credentials for Login
        admin_credentials = {
            'admin':'admin@gmail.com',
            'password':'admin@123'
        }

        create_admin(admin_email = admin_credentials['admin'],admin_password = admin_credentials['password'])

    #Web Routes Blueprint
    from app.routes.web import index_bp
    app.register_blueprint(index_bp,url_prefix='/')


    #Api Routes Blueprint
    from app.routes.api import users_bp
    app.register_blueprint(users_bp,url_prefix='/user')

    #admin Routes Blueprint
    from app.routes.web import admin_bp
    app.register_blueprint(admin_bp,url_prefix='/admin')

    return app







