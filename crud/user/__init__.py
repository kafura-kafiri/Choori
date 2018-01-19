from sanic import Blueprint
bp = Blueprint('user')
from config import users

import crud.user.authentication
