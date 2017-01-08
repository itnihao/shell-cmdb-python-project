#-*- coding: UTF-8 -*-
from flask import Blueprint, render_template
from flask_login import login_required

server = Blueprint('server', __name__)


@server.route("/")
@login_required
def index():
    return render_template("server.html")


@server.route("/list")
@login_required
def list():
    return "列表页需要认证"