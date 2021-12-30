from flask import redirect, Blueprint, url_for, render_template, request, flash, session
import sqlite3
import os
from . import admin_pswd
from . import allowed_file
from .models import UserAdmin
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin
from datetime import datetime

admin = Blueprint('admin', __name__)

UPLOAD_FOLDER = 'MMC2/website/static/data/miniature/'

@admin.route('/login', methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('public.home'))
    if request.method == 'POST':
        db = sqlite3.connect('MMC2/website/data.db')
        cur = db.cursor()
        username = request.form.get('username')
        password = request.form.get('password')
        cur.execute("SELECT EXISTS(SELECT * FROM 'AdminUser' WHERE username=?)",(username,))
        if cur.fetchone()[0]==1:
            cur.execute("SELECT * FROM 'AdminUser' WHERE username=?",(username,))
            user = list(cur.fetchone())
            if user[2] == password :

                login_user(UserAdmin(int(user[0]), user[1], user[2]), remember=True)
                flash(f'Bonjour ! Vous êtes connecté en tant que {user[1]}.', category='success')
                return redirect(url_for('admin.adminhome'))
            else :
                flash(f'Mot de passe incorrect', category = 'error')
        else :
            flash(f'Utilisateur inconnu', category = 'error')
    return render_template('ADMINlogin.html')


@admin.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('public.home'))


@admin.route('/newadmin', methods = ['GET', 'POST'])
@login_required
def newadmin():
    if request.method == 'POST':
        db = sqlite3.connect('MMC2/website/data.db')
        cur = db.cursor()
        adminpswd = request.form.get('adminpswd')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        cur.execute("SELECT EXISTS(SELECT * FROM 'AdminUser' WHERE username=?)",(username,))
        if cur.fetchone()[0]==1:
            flash('Utilisateur dejà existant', category = 'error')
        elif password1 != password2 :
            flash('Les mots de passes ne concordent pas', category = 'error')
        elif adminpswd != admin_pswd:
            flash(f'Mot de passe Admin incorrect', category = 'error')
        else :
            cur.execute("INSERT INTO AdminUser (username,password) VALUES(?,?)",(username,password1,))
            db.commit()
            return redirect(url_for('admin.login'))
    return render_template('ADMINnewadmin.html')

@admin.route('/', methods = ['GET', 'POST'])
@login_required
def adminhome():
    db = sqlite3.connect('MMC2/website/data.db')
    cur = db.cursor()
    cur.execute("SELECT * FROM posts ORDER BY id DESC")
    listeposts = list(cur.fetchall())
    return render_template('ADMINhome.html', listeposts=listeposts)

@admin.route('/delete/<nompost>', methods = ['GET', 'POST'])
@login_required
def delete(nompost):
    nompost = nompost.replace("-", " ")
    if request.method == 'POST':
        nompost = nompost.replace("-", " ")
        db = sqlite3.connect('MMC2/website/data.db')
        cur = db.cursor()
        cur.execute("DELETE FROM posts WHERE nom=?",(nompost,))
        db.commit()
        return redirect(url_for('admin.adminhome'))
    db = sqlite3.connect('MMC2/website/data.db')
    cur = db.cursor()
    cur.execute("SELECT EXISTS(SELECT * FROM posts WHERE nom=?)",(nompost,))
    if cur.fetchone()[0]==1:
        cur.execute("SELECT * FROM posts WHERE nom=?",(nompost,))
        post = list(cur.fetchone())
        return render_template('ADMINdelete.html', post=post)
    else :
        flash("Ce post n'existe pas", category = 'error')
        return redirect(url_for('admin.adminhome'))


@admin.route('/newvideo', methods = ['GET', 'POST'])
@login_required
def newvideo():
    if request.method == 'POST':
        db = sqlite3.connect('MMC2/website/data.db')
        cur = db.cursor()
        title = request.form.get('title')
        cur.execute("SELECT EXISTS(SELECT * FROM posts WHERE nom=?)",(title,))
        if cur.fetchone()[0]==1:
            flash('Titre de post déjà utilisé', category = 'error')
        else :
            subtitle = request.form.get('subtitle')
            description = request.form.get('descritpion')
            if description == None:
                description = ''
            author = request.form.get('author')
            link = request.form.get('link').replace("watch?v=", "embed/")
            if len(link)<4:
                flash('Lien invalide', category = 'error')
            else :
                file = request.files['file']
                if file.filename == '':
                    flash('Pas de miniature sélectionnée', category = 'error')
                elif file and allowed_file(file.filename):
                    filename = file.filename
                    file.save(os.path.join(UPLOAD_FOLDER , filename))
                    now = datetime.now() # current date and time
                    date = now.strftime("%d/%m/%Y")
                    type = 'video'
                    db = sqlite3.connect('MMC2/website/data.db')
                    cur = db.cursor()
                    cur.execute("INSERT INTO posts (type,Nom,date,auteurs,Soustitre,paragraphe,miniature,lien) VALUES (?,?,?,?,?,?,?,?)",(type,title,date,author,subtitle,description,filename,link,))
                    db.commit()
                    return redirect(url_for('admin.adminhome'))

    return render_template('ADMINnewvideo.html')
