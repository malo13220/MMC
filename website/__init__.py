from flask import Flask, render_template
import sqlite3
from os import path
from flask_login import LoginManager


UPLOAD_FOLDER = '/data/miniature'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
public_pswd = 'Marcus_forever'
admin_pswd = 'admin'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY']='secretkey'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    from .public import public
    from .admin import admin
    from .models import UserAdmin

    app.register_blueprint(public, url_prefix='/')
    app.register_blueprint(admin, url_prefix='/admin')

    login_manager = LoginManager()
    login_manager.login_view = "admin.login" #attention pas bon
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        db = sqlite3.connect('MMC2/website/data.db')
        cur = db.cursor()
        cur.execute("SELECT * FROM AdminUser WHERE id = (?)",[user_id])
        lu = cur.fetchone()
        if lu is None:
            return None
        else:
            return UserAdmin(int(lu[0]), lu[1], lu[2])


    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    return app
