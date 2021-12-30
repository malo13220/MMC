from flask import redirect, Blueprint, url_for, render_template, request, flash, session
import sqlite3
from . import admin_pswd
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin


class UserAdmin(UserMixin):
    def __init__(self, id, email, password):
         self.id = id
         self.email = email
         self.password = password
         self.authenticated = False
