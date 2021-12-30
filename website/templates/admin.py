'''
Pages admin
'''

from flask import redirect, Blueprint, url_for, render_template, request, flash, session
from . import db
from .models import UserAdmin
from . import admin_pswd
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

admin = Blueprint('admin', __name__)

@admin.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get("username")
        pswd = request.form.get('password')

        user = UserAdmin.query.filter_by(username=username).first()
        if user :
            if check_password_hash(user.password, pswd):
                login_user(user, remember=True)
                return redirect(url_for('admin.home'))
            else :
                flash('Mot de passe incorrect', category='error')
        else :
            flash('Username incorrect', category='error')
    return render_template("loginadmin.html")


@admin.route('/newadmin', methods = ['GET', 'POST'])
def newadmin():
    if request.method == 'POST':
        adminpswd = request.form.get('passwordadmin')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        username_exists = UserAdmin.query.filter_by(username=username).first()
        if adminpswd != admin_pswd:
            flash('Mot de passer Admin incorrect', category = 'error')
        elif username_exists:
            flash('Username dejà existant', category = 'error')
        elif password1 != password2:
            flash('Les mots de passes ne sont pas les mêmes !', category = 'error')
        else :
            new_user = UserAdmin(username = username, password = generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash('Utilisateur Admin créé')
            return redirect(url_for("admin.login"))
    return render_template("signupadmin.html")

@admin.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('public.home'))


@admin.route('/')
@login_required
def home():
    return '<h1>Admin</h1>'
