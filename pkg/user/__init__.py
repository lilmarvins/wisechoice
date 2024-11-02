from flask import Blueprint



userobj = Blueprint('bpuser',__name__, template_folder='templates', static_folder='static', url_prefix='/home/')



# routes
# to make the loacl routes avaulabe in this package
from . import user_routes