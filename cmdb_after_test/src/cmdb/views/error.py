#-*- coding: UTF-8 -*-

from flask import Blueprint, render_template
from flask_login import login_required

error = Blueprint('error', __name__)

@error.route("/")
@login_required
def index():
    msg = 'You have no permission to access the resource.'
    title = 'Forbidden.'
    return render_template("error.html",status = 403,title = title, msg = msg)
