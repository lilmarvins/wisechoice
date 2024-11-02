from flask import Blueprint,render_template,session
from pkg.models import Admin,db


errorbp = Blueprint('errors',__name__, template_folder='templates')



