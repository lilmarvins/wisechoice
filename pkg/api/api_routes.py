from flask import render_template,session,url_for,redirect,request,flash
from . import apiobj

@apiobj.route("/vv/")
def user_home():
    return "this is api"

