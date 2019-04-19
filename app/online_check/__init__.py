
from flask import Blueprint
bp = Blueprint('online_check', __name__)

from app.online_check import routes


