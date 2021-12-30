from flask import redirect, Blueprint, url_for, render_template, request, flash, session
from . import public_pswd
import sqlite3


public = Blueprint('public', __name__)
id = 0

@public.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        pswd = request.form.get('password')
        if pswd == public_pswd:
            session['id'] = id +1
            return redirect(url_for('public.home'))
        else :
            flash('Mauvais mot de passe', category='error')
    return render_template("login.html")

@public.route('/')
def home():
    if 'id' in session :
        db = sqlite3.connect('MMC2/website/data.db')
        cur = db.cursor()
        cur.execute("SELECT * FROM posts ORDER BY id DESC")
        listeposts = list(cur.fetchall())
        return render_template('home.html', listeposts=listeposts)
    else :
        return redirect(url_for('public.login'))

@public.route('/videos')
def videos():
    if 'id' in session :
        db = sqlite3.connect('MMC2/website/data.db')
        cur = db.cursor()
        cur.execute("SELECT * FROM posts WHERE type='video' ORDER BY id DESC")
        listeposts = list(cur.fetchall())
        return render_template('videos.html', listeposts=listeposts)
    else :
        return redirect(url_for('public.login'))

@public.route('/photos')
def photos():
    if 'id' in session :
        db = sqlite3.connect('MMC2/website/data.db')
        cur = db.cursor()
        cur.execute("SELECT * FROM posts WHERE type='photos' ORDER BY id DESC")
        listeposts = list(cur.fetchall())
        return render_template('photos.html', listeposts=listeposts)
    else :
        return redirect(url_for('public.login'))

@public.route('/articles')
def articles():
    if 'id' in session :
        db = sqlite3.connect('MMC2/website/data.db')
        cur = db.cursor()
        cur.execute("SELECT * FROM posts WHERE type='articles' ORDER BY id DESC")
        listeposts = list(cur.fetchall())
        return render_template('articles.html', listeposts=listeposts)
    else :
        return redirect(url_for('public.login'))



@public.route('/post/<nompost>')
def post(nompost):
    nompost = nompost.replace("-", " ")
    db = sqlite3.connect('MMC2/website/data.db')
    cur = db.cursor()
    cur.execute("SELECT EXISTS(SELECT * FROM posts WHERE nom=?)",(nompost,))
    if cur.fetchone()[0]==1:
        cur.execute("SELECT * FROM posts WHERE nom=?",(nompost,))
        post = list(cur.fetchone())
        if post[1] == 'video':
            return render_template('postvideo.html', post=post)
    else :
        return redirect(url_for('public.home'))
