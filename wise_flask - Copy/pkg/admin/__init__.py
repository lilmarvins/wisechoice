from flask import Blueprint



adminobj = Blueprint('bpadmin',__name__, template_folder='templates', static_folder='static', url_prefix="/admin/")



# routes
# to make the loacl routes avaulabe in this package
from . import adminroutes