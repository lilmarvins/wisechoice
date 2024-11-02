from flask import Blueprint



apiobj = Blueprint('bpapi',__name__)



# routes
# to make the loacl routes avaulabe in this package
from . import api_routes