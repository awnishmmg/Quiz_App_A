from flask import render_template, request,jsonify,session,flash,redirect,url_for
from flask_bcrypt import Bcrypt
import re
from app.models import create_user,get_users_list,get_user_details,update_user_details,getuser_count,delete_user

bcrypt = Bcrypt()

def dashboard_page():
    return render_template('user/dashboard.html')